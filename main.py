#!/usr/bin/env python3
"""SeedwaveCore CLI — boot the unified Fruitful/NoodleNexus ecosystem."""

from __future__ import annotations

import argparse
import logging
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("seedwave")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="SeedwaveCore™ — Fruitful Ecosystem Entry Point",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Boot full ecosystem with 9s heartbeat
  python main.py --demo       # Run NoodleNexus demo and exit
  python main.py --webhook    # Start webhook server only (no heartbeat)
  python main.py --port 5001  # Webhook on custom port

Genesis: SEEDWAVE-011-CORE (Heyns Schoeman, 2025-04-08)
""",
    )
    parser.add_argument("--demo", action="store_true", help="Run NoodleNexus demo then exit")
    parser.add_argument("--webhook", action="store_true", help="Start webhook server (standalone)")
    parser.add_argument("--port", type=int, default=5000, help="Webhook port (default: 5000)")
    parser.add_argument("--no-heartbeat", action="store_true", help="Disable the 9s VaultMesh pulse")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = parser.parse_args()

    logging.getLogger().setLevel(args.log_level)

    if args.demo:
        _run_demo()
        return

    if args.webhook:
        _run_webhook_only(port=args.port)
        return

    _run_full(port=args.port, heartbeat=not args.no_heartbeat)


def _run_demo() -> None:
    from core.seedwave_core import SeedwaveCore

    logger.info("=== SEEDWAVE-011-CORE DEMO MODE ===")
    sc = SeedwaveCore()
    state = sc.get_state()
    logger.info("Genesis signal: %s", state["genesis"]["id"])

    nexus = sc.nexus
    logger.info("Running NoodleNexus demo...")
    nexus.run_demo()

    metrics = nexus.get_comprehensive_metrics()
    logger.info("Pulse metrics: %s", metrics.get("pulse_trade", {}))
    logger.info("Claim metrics: %s", metrics.get("claim_root", {}))
    logger.info("Demo complete.")


def _run_webhook_only(port: int) -> None:
    from webhook.fruitful_webhook import FruitfulWebhook
    import os

    secret = os.getenv("WEBHOOK_SECRET")
    wh = FruitfulWebhook(secret=secret, port=port)

    @wh.on("push")
    def on_push(event):
        repo = event.payload.get("repository", {}).get("full_name", "unknown")
        ref = event.payload.get("ref", "")
        logger.info("[PUSH] %s → %s", repo, ref)

    @wh.on("ping")
    def on_ping(event):
        logger.info("[PING] zen: %s", event.payload.get("zen", ""))

    logger.info("Starting standalone webhook server on port %d", port)
    wh.start()


def _run_full(port: int, heartbeat: bool) -> None:
    from core.seedwave_core import SeedwaveCore

    sc = SeedwaveCore()
    sc.boot(webhook_port=port)


if __name__ == "__main__":
    main()
