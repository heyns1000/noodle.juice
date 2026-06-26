"""FruitfulWebhook — standalone Flask webhook handler for Fruitful/HotStack ecosystem events."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

try:
    from flask import Flask, request, jsonify
except ImportError:
    Flask = None  # type: ignore

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    PUSH = "push"
    PULL_REQUEST = "pull_request"
    RELEASE = "release"
    DEPLOYMENT = "deployment"
    WORKFLOW_RUN = "workflow_run"
    ISSUES = "issues"
    PING = "ping"
    # Fruitful-specific
    HOTSTACK_UPLOAD = "hotstack.upload"
    HOTSTACK_DEPLOY = "hotstack.deploy"
    BUILDNEST_BUILD = "buildnest.build"
    VAULTMESH_PULSE = "vaultmesh.pulse"
    CLAIMROOT_CAST = "claimroot.cast"
    BARECART_ORDER = "barecart.order"


@dataclass
class WebhookEvent:
    event_type: str
    payload: Dict[str, Any]
    delivery_id: str
    received_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    source: str = "github"
    verified: bool = False
    processed: bool = False
    error: Optional[str] = None


class FruitfulWebhook:
    """Standalone webhook server for Fruitful ecosystem events."""

    def __init__(
        self,
        secret: Optional[str] = None,
        port: int = 5001,
        host: str = "0.0.0.0",
    ):
        self.secret = secret or os.getenv("WEBHOOK_SECRET", "")
        self.port = port
        self.host = host
        self._handlers: Dict[str, List[Callable]] = {}
        self._events: List[WebhookEvent] = []
        self._stats = {
            "received": 0,
            "verified": 0,
            "failed_auth": 0,
            "processed": 0,
            "errors": 0,
        }
        self._app: Optional[Any] = None
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Handler registration
    # ------------------------------------------------------------------

    def on(self, event_type: str) -> Callable:
        """Decorator: @webhook.on('push')"""
        def decorator(fn: Callable) -> Callable:
            self._handlers.setdefault(event_type, []).append(fn)
            logger.debug("Registered handler for '%s': %s", event_type, fn.__name__)
            return fn
        return decorator

    def register(self, event_type: str, handler: Callable) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    # ------------------------------------------------------------------
    # Signature verification
    # ------------------------------------------------------------------

    def _verify(self, body: bytes, signature: str) -> bool:
        if not self.secret:
            return True  # no secret configured — accept all
        if not signature.startswith("sha256="):
            return False
        expected = "sha256=" + hmac.new(
            self.secret.encode(), body, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    def _dispatch(self, event: WebhookEvent) -> None:
        handlers = self._handlers.get(event.event_type, []) + self._handlers.get("*", [])
        for handler in handlers:
            try:
                handler(event)
                event.processed = True
                with self._lock:
                    self._stats["processed"] += 1
            except Exception as exc:
                event.error = str(exc)
                with self._lock:
                    self._stats["errors"] += 1
                logger.error("Handler error for '%s': %s", event.event_type, exc)

    # ------------------------------------------------------------------
    # Flask app
    # ------------------------------------------------------------------

    def build_app(self) -> Any:
        if Flask is None:
            raise RuntimeError("Flask is not installed. Run: pip install flask")

        app = Flask(__name__)

        @app.route("/webhook", methods=["POST"])
        def handle_webhook():
            body = request.get_data()
            sig = request.headers.get("X-Hub-Signature-256", "")
            event_type = request.headers.get("X-GitHub-Event", "unknown")
            delivery_id = request.headers.get("X-GitHub-Delivery", "unknown")

            with self._lock:
                self._stats["received"] += 1

            verified = self._verify(body, sig)
            if sig and not verified:
                with self._lock:
                    self._stats["failed_auth"] += 1
                logger.warning("Rejected webhook delivery %s — bad signature", delivery_id)
                return jsonify({"error": "invalid signature"}), 401

            if verified:
                with self._lock:
                    self._stats["verified"] += 1

            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                return jsonify({"error": "invalid JSON"}), 400

            event = WebhookEvent(
                event_type=event_type,
                payload=payload,
                delivery_id=delivery_id,
                verified=verified,
            )

            with self._lock:
                self._events.append(event)
                if len(self._events) > 1000:  # rolling window
                    self._events = self._events[-1000:]

            threading.Thread(target=self._dispatch, args=(event,), daemon=True).start()

            return jsonify({"status": "accepted", "delivery_id": delivery_id}), 202

        @app.route("/health", methods=["GET"])
        def health():
            return jsonify({"status": "ok", "service": "fruitful-webhook", "stats": self._stats})

        @app.route("/events", methods=["GET"])
        def events():
            with self._lock:
                recent = [
                    {
                        "event_type": e.event_type,
                        "delivery_id": e.delivery_id,
                        "received_at": e.received_at,
                        "verified": e.verified,
                        "processed": e.processed,
                        "error": e.error,
                    }
                    for e in self._events[-50:]
                ]
            return jsonify({"events": recent, "total": len(self._events)})

        @app.route("/", methods=["GET"])
        def index():
            return jsonify({
                "service": "Fruitful Webhook Server",
                "version": "1.0.0",
                "genesis": "SEEDWAVE-011-CORE",
                "endpoints": ["/webhook", "/health", "/events"],
            })

        self._app = app
        return app

    def start(self, debug: bool = False) -> None:
        app = self.build_app()
        logger.info("FruitfulWebhook starting on %s:%d", self.host, self.port)
        app.run(host=self.host, port=self.port, debug=debug)

    def start_threaded(self) -> threading.Thread:
        app = self.build_app()
        t = threading.Thread(
            target=lambda: app.run(host=self.host, port=self.port, debug=False, use_reloader=False),
            daemon=True,
            name="fruitful-webhook",
        )
        t.start()
        return t

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._stats)


def create_app(secret: Optional[str] = None) -> Any:
    """Factory for WSGI deployment."""
    wh = FruitfulWebhook(secret=secret)
    return wh.build_app()
