"""
SyncBridge™ — GitHub Webhook ↔ PulseTrade™ Integration

Every GitHub push enqueues file tasks.
Every 9-second SYNC pulse drains the queue into Cloudflare R2.

  GitHub Push → POST /webhook → queue → SYNC pulse → R2

This is the nervous system between the outside world (GitHub)
and the inner ecosystem (PulseTrade™ + R2 storage).
"""
import os
import hmac
import hashlib
import threading
from collections import deque
from datetime import datetime
from typing import Dict, Any, Optional, TYPE_CHECKING

try:
    import requests
    import boto3
    from botocore.client import Config
    from flask import Flask, request, jsonify
    _DEPS = True
except ImportError:
    _DEPS = False

from systems.pulsetrade import Pulse

SOURCE_MAP = {
    "heyns1000": "heyns1000-repos",
    "fruitful-global-planet": "fruitful-global-planet",
}

BUCKET = os.getenv("R2_BUCKET", "fruitful-thank-you")
BASE_PATH = "fruitful-git-thank-you"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID", "")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY", "")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY", "")


class SyncBridge:
    """
    Bridges GitHub webhook events with PulseTrade™ SYNC pulses.
    Queue depth is drained on each 9-second SYNC beat.
    Files sync to Cloudflare R2 using the fruitful-thank-you bucket structure.
    """

    def __init__(self, nexus):
        self.nexus = nexus
        self._queue: deque = deque()
        self._stats: Dict[str, int] = {
            "total_push_events": 0,
            "files_synced": 0,
            "files_deleted": 0,
            "errors": 0,
        }
        self._r2 = self._build_r2()
        self._gh_headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "SeedwaveCore-SyncBridge/1.0",
        }
        if _DEPS:
            self._app = self._build_app()

    def _build_r2(self):
        if not _DEPS or not all([R2_ACCOUNT_ID, R2_ACCESS_KEY, R2_SECRET_KEY]):
            return None
        return boto3.client(
            "s3",
            endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY,
            config=Config(signature_version="s3v4"),
        )

    def _build_app(self):
        app = Flask("seedwave-sync-bridge")

        @app.route("/webhook", methods=["POST"])
        def webhook():
            sig = request.headers.get("X-Hub-Signature-256", "")
            if not self._verify(request.data, sig):
                return jsonify({"error": "Invalid signature"}), 401
            event = request.headers.get("X-GitHub-Event", "")
            if event == "ping":
                return jsonify({"message": "\U0001f331 SEEDWAVE-011-CORE webhook active"}), 200
            if event == "push":
                self._enqueue_push(request.json)
                return jsonify({
                    "queued": True,
                    "queue_depth": len(self._queue),
                }), 200
            return jsonify({"ignored": event}), 200

        @app.route("/health")
        def health():
            return jsonify({
                "status": "healthy",
                "signal": "SEEDWAVE-011-CORE",
                "queue_depth": len(self._queue),
                "r2_connected": self._r2 is not None,
                "stats": self._stats,
                "timestamp": datetime.now().isoformat(),
            })

        @app.route("/")
        def index():
            return jsonify({
                "service": "SeedwaveCore™ SyncBridge",
                "signal_id": "SEEDWAVE-011-CORE",
                "bucket": f"r2://{BUCKET}/{BASE_PATH}/",
                "sources": list(SOURCE_MAP.keys()),
            })

        return app

    def _verify(self, body: bytes, sig: str) -> bool:
        if not WEBHOOK_SECRET:
            return True
        expected = "sha256=" + hmac.new(
            WEBHOOK_SECRET.encode(), body, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, sig)

    def _enqueue_push(self, payload: Dict):
        owner = payload["repository"]["owner"]["login"]
        repo = payload["repository"]["name"]
        branch = payload["ref"].replace("refs/heads/", "")
        self._stats["total_push_events"] += 1
        for commit in payload.get("commits", []):
            sha = commit["id"]
            for path in commit.get("added", []) + commit.get("modified", []):
                self._queue.append({"action": "put", "owner": owner, "repo": repo, "branch": branch, "path": path, "sha": sha})
            for path in commit.get("removed", []):
                self._queue.append({"action": "delete", "owner": owner, "repo": repo, "path": path})

    async def handle_sync_pulse(self, pulse: Pulse) -> Dict:
        """Drain the sync queue on every PulseTrade™ SYNC beat."""
        processed = 0
        while self._queue:
            task = self._queue.popleft()
            try:
                if task["action"] == "put":
                    self._put(task)
                    self._stats["files_synced"] += 1
                else:
                    self._delete(task)
                    self._stats["files_deleted"] += 1
                processed += 1
            except Exception as exc:
                self._stats["errors"] += 1
                self._queue.appendleft(task)
                print(f"  ⚠️  SyncBridge error (will retry): {exc}")
                break
        return {"pulse_id": pulse.pulse_id, "processed": processed, "queue_remaining": len(self._queue)}

    def _put(self, task: Dict):
        if not self._r2 or not _DEPS:
            print(f"  [DRY] sync {task['owner']}/{task['repo']}/{task['path']}")
            return
        url = f"https://raw.githubusercontent.com/{task['owner']}/{task['repo']}/{task['branch']}/{task['path']}"
        resp = requests.get(url, headers=self._gh_headers, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"GitHub {resp.status_code}: {url}")
        folder = SOURCE_MAP.get(task["owner"], task["owner"])
        self._r2.put_object(
            Bucket=BUCKET,
            Key=f"{BASE_PATH}/{folder}/{task['repo']}/{task['path']}",
            Body=resp.content,
            Metadata={"github-sha": task["sha"], "sync-time": str(int(datetime.now().timestamp()))},
        )

    def _delete(self, task: Dict):
        if not self._r2 or not _DEPS:
            print(f"  [DRY] delete {task['owner']}/{task['repo']}/{task['path']}")
            return
        folder = SOURCE_MAP.get(task["owner"], task["owner"])
        self._r2.delete_object(Bucket=BUCKET, Key=f"{BASE_PATH}/{folder}/{task['repo']}/{task['path']}")

    def start_webhook_server(self, host: str = "0.0.0.0", port: int = 5000):
        if not _DEPS:
            print("  ⚠️  Flask/requests/boto3 not installed — webhook disabled")
            return
        print(f"\U0001f517  SyncBridge webhook: http://{host}:{port}/webhook")
        self._app.run(host=host, port=port, debug=False, use_reloader=False)

    def get_queue_depth(self) -> int:
        return len(self._queue)

    def get_stats(self) -> Dict:
        return dict(self._stats)
