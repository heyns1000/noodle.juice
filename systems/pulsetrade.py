"""
PulseTrade™ (9秒脈衝)
刻字問天 - Engraving Question Heaven

"9 seconds per move, multiply by 10,000"
9秒一子, 乘以一萬
"""

import time
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum


class PulseType(Enum):
    HEARTBEAT = "heartbeat"
    TRADE = "trade"
    SYNC = "sync"
    CLAIM = "claim"
    BACKUP = "backup"
    METRIC = "metric"


class PulseStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Pulse:
    pulse_id: str
    pulse_type: PulseType
    timestamp: float
    interval: float = 9.0
    data: Dict[str, Any] = field(default_factory=dict)
    status: PulseStatus = PulseStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "pulse_id": self.pulse_id,
            "pulse_type": self.pulse_type.value,
            "timestamp": self.timestamp,
            "interval": self.interval,
            "data": self.data,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
        }


@dataclass
class PulseSequence:
    sequence_id: str
    pulses: List[Pulse] = field(default_factory=list)
    multiplier: int = 10000
    total_cycles: int = 0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None


class PulseTrade:
    """
    PulseTrade™ System
    Rhythmic transaction and synchronization protocol based on 9-second pulses.
    刻字問天 - Every 9 seconds, we engrave our question to heaven.
    """

    def __init__(self, pulse_interval: float = 9.0):
        self.pulse_interval = pulse_interval
        self.pulses: Dict[str, Pulse] = {}
        self.sequences: Dict[str, PulseSequence] = {}
        self.handlers: Dict[PulseType, List[Callable]] = {pt: [] for pt in PulseType}
        self.running = False
        self.pulse_count = 0
        self.start_time: Optional[float] = None

    def register_handler(self, pulse_type: PulseType, handler: Callable):
        self.handlers[pulse_type].append(handler)

    def create_pulse(self, pulse_type: PulseType, data=None, interval=None) -> Pulse:
        timestamp = time.time()
        pulse_id = f"{pulse_type.value}_{timestamp}_{self.pulse_count}"
        pulse = Pulse(
            pulse_id=pulse_id, pulse_type=pulse_type, timestamp=timestamp,
            interval=interval or self.pulse_interval, data=data or {},
        )
        self.pulses[pulse_id] = pulse
        self.pulse_count += 1
        return pulse

    async def execute_pulse(self, pulse: Pulse) -> Pulse:
        pulse.status = PulseStatus.ACTIVE
        try:
            handlers = self.handlers.get(pulse.pulse_type, [])
            if not handlers:
                pulse.status = PulseStatus.SKIPPED
                return pulse
            results = []
            for handler in handlers:
                try:
                    results.append(await handler(pulse))
                except Exception as e:
                    pulse.error = str(e)
                    pulse.status = PulseStatus.FAILED
                    return pulse
            pulse.result = results
            pulse.status = PulseStatus.COMPLETED
        except Exception as e:
            pulse.error = str(e)
            pulse.status = PulseStatus.FAILED
        return pulse

    def create_sequence(self, sequence_id, pulse_types, cycles=1, multiplier=10000) -> PulseSequence:
        sequence = PulseSequence(sequence_id=sequence_id, multiplier=multiplier, total_cycles=cycles)
        for cycle in range(cycles):
            for pt in pulse_types:
                pulse = self.create_pulse(pt, data={"cycle": cycle, "sequence_id": sequence_id})
                sequence.pulses.append(pulse)
        self.sequences[sequence_id] = sequence
        return sequence

    async def run_sequence(self, sequence_id: str) -> PulseSequence:
        if sequence_id not in self.sequences:
            raise ValueError(f"Sequence {sequence_id} not found")
        sequence = self.sequences[sequence_id]
        sequence.started_at = time.time()
        for pulse in sequence.pulses:
            await self.execute_pulse(pulse)
            await asyncio.sleep(pulse.interval)
        sequence.completed_at = time.time()
        return sequence

    async def start_heartbeat(self, handlers=None):
        if handlers:
            for h in handlers:
                self.register_handler(PulseType.HEARTBEAT, h)
        self.running = True
        self.start_time = time.time()
        print(f"\U0001f493 PulseTrade™ Heartbeat Started")
        print(f"⏱️  Pulse Interval: {self.pulse_interval}s")
        print(f"\U0001f537 九天之脈已開 (Nine Heaven Pulse Opened)\n")
        while self.running:
            pulse = self.create_pulse(
                PulseType.HEARTBEAT,
                data={"uptime": time.time() - self.start_time, "pulse_count": self.pulse_count},
            )
            await self.execute_pulse(pulse)
            print(f"\U0001f493 Pulse #{self.pulse_count} | {pulse.status.value} | {datetime.now().strftime('%H:%M:%S')}")
            await asyncio.sleep(self.pulse_interval)

    def stop_heartbeat(self):
        self.running = False

    def get_pulse_metrics(self) -> Dict[str, Any]:
        by_status: Dict[str, int] = {}
        by_type: Dict[str, int] = {}
        for p in self.pulses.values():
            by_status[p.status.value] = by_status.get(p.status.value, 0) + 1
            by_type[p.pulse_type.value] = by_type.get(p.pulse_type.value, 0) + 1
        return {
            "total_pulses": len(self.pulses),
            "by_status": by_status,
            "by_type": by_type,
            "uptime": time.time() - self.start_time if self.start_time else 0,
            "pulse_interval": self.pulse_interval,
        }

    def export_pulses(self) -> Dict[str, Any]:
        return {
            "pulses": [p.to_dict() for p in self.pulses.values()],
            "sequences": {
                sid: {"sequence_id": s.sequence_id, "pulse_count": len(s.pulses), "multiplier": s.multiplier}
                for sid, s in self.sequences.items()
            },
            "metrics": self.get_pulse_metrics(),
            "export_timestamp": datetime.now().isoformat(),
        }


class PulseTradeFactory:
    @staticmethod
    async def create_sync_pulse(pulsetrade, source, destination, data=None):
        data = data or {}
        data.update({"source": source, "destination": destination})
        pulse = pulsetrade.create_pulse(PulseType.SYNC, data=data)
        return await pulsetrade.execute_pulse(pulse)

    @staticmethod
    async def create_backup_pulse(pulsetrade, backup_type, targets, data=None):
        data = data or {}
        data.update({"backup_type": backup_type, "targets": targets})
        pulse = pulsetrade.create_pulse(PulseType.BACKUP, data=data)
        return await pulsetrade.execute_pulse(pulse)

    @staticmethod
    def create_trading_sequence(pulsetrade, sequence_id, trades=10000):
        return pulsetrade.create_sequence(
            sequence_id=sequence_id,
            pulse_types=[PulseType.TRADE, PulseType.METRIC],
            cycles=trades, multiplier=10000,
        )
