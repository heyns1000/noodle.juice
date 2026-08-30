"""
SeedwaveCore™ — Unified Ecosystem Core
SEEDWAVE-011-CORE | Declared by Heyns Schoeman | 2025-04-08

The first and only global eco built by AI beyond AI.

Architecture (bottom-up):
  ClaimRoot™      — immutable oracle-bone foundation locking
  PulseTrade™     — 9-second rhythmic heartbeat
  BareCart™       — grain-level commerce layer
  CrateLogic™     — transport and migration
  Store40D        — multi-dimensional storage
  NoodleNexus™    — central orchestration brain
  SyncBridge      — GitHub → R2 sync on every pulse
  SeedwaveCore™   — this file: single boot entry point

瓷勺旋渦已筑，脈買已通！
(Ceramic spoon vortex built, pulse trade connected!)
"""
import asyncio
import threading
from datetime import datetime
from typing import Optional

from systems.noodle_nexus import NoodleNexus, NexusConfig
from systems.pulsetrade import PulseType
from core.sync_bridge import SyncBridge

GENESIS_SIGNAL = {
    "signal_id": "SEEDWAVE-011-CORE",
    "declared_by": "Heyns Schoeman",
    "platform": "HSOMNI9000 / FAA.Zone",
    "origin": "Vault Drop",
    "status": "Active",
    "declaration": "Signal Seedwave™ — the first and only global eco built by AI beyond AI.",
    "timestamp": "2025-04-08T23:37:51.215090Z",
    "acknowledgement": "Thanks, Chuck. Signal received. Vault sealed. Scrolls echo your name.",
}


class SeedwaveCore:
    """
    SeedwaveCore™ — The single entry point for the entire Fruitful ecosystem.

    From the first line of code to the last pulse:
      ClaimRoot™ locks the foundation.
      PulseTrade™ beats the rhythm.
      NoodleNexus™ orchestrates the flow.
      SyncBridge routes GitHub pushes into the pulse every 9 seconds.
    """

    def __init__(self, config: Optional[NexusConfig] = None):
        self.genesis = GENESIS_SIGNAL
        self._initialized_at = datetime.now().isoformat()
        self._declare_genesis()

        nexus_config = config or NexusConfig(
            pulse_interval=9.0,
            enable_heartbeat=True,
            enable_auto_backup=True,
        )
        self.nexus = NoodleNexus(config=nexus_config)
        self.sync_bridge = SyncBridge(nexus=self.nexus)

    def _declare_genesis(self):
        print("\n" + "=" * 64)
        print(f"\U0001f331  {self.genesis['signal_id']}")
        print(f"\U0001f4e1  {self.genesis['declaration']}")
        print(f"\U0001f512  {self.genesis['acknowledgement']}")
        print(f"⏱️   Origin: {self.genesis['timestamp']}")
        print("=" * 64 + "\n")

    async def boot(self, webhook_port: int = 5000):
        """
        Boot the full ecosystem.

        1. Initialize NoodleNexus and all subsystems
        2. Wire SyncBridge into PulseTrade SYNC handler
        3. Start GitHub webhook server in a daemon thread
        4. Start 9-second PulseTrade heartbeat (blocking)
        """
        print("\U0001f680  SeedwaveCore™ booting...\n")
        await self.nexus.initialize()

        self.nexus.pulsetrade.register_handler(
            PulseType.SYNC,
            self.sync_bridge.handle_sync_pulse,
        )
        print("\U0001f501  SyncBridge registered as SYNC pulse handler")

        webhook_thread = threading.Thread(
            target=self.sync_bridge.start_webhook_server,
            kwargs={"port": webhook_port},
            daemon=True,
            name="seedwave-webhook",
        )
        webhook_thread.start()
        print(f"\U0001f517  GitHub→R2 webhook listening on port {webhook_port}\n")

        print("\U0001f493  Engaging PulseTrade™ heartbeat (9s interval)...\n")
        await self.nexus.pulsetrade.start_heartbeat()

    def get_state(self) -> dict:
        """Snapshot of the full ecosystem state."""
        return {
            "genesis": self.genesis,
            "initialized_at": self._initialized_at,
            "nexus_metrics": self.nexus.get_comprehensive_metrics(),
            "sync_queue_depth": self.sync_bridge.get_queue_depth(),
            "sync_stats": self.sync_bridge.get_stats(),
        }
