"""Store40D — 40-dimensional key-value storage for the Fruitful ecosystem."""

from __future__ import annotations

import hashlib
import json
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class DimensionType(str, Enum):
    BRAND = "brand"
    ASSET = "asset"
    LICENSE = "license"
    USER = "user"
    PAYMENT = "payment"
    SIGNAL = "signal"
    BUILD = "build"
    DEPLOY = "deploy"
    PULSE = "pulse"
    METRIC = "metric"
    CLAIM = "claim"
    VAULT = "vault"
    CART = "cart"
    ORDER = "order"
    REPO = "repo"
    WEBHOOK = "webhook"
    CRATE = "crate"
    SYNC = "sync"
    HEALTH = "health"
    LOG = "log"
    CONFIG = "config"
    SECRET = "secret"
    TOKEN = "token"
    SESSION = "session"
    AUDIT = "audit"
    ROYALTY = "royalty"
    GLYPH = "glyph"
    GRAIN = "grain"
    TERRITORY = "territory"
    SECTOR = "sector"
    PARTNER = "partner"
    CONTRACT = "contract"
    TEMPLATE = "template"
    DOMAIN = "domain"
    EMAIL = "email"
    MEDIA = "media"
    EVENT = "event"
    TASK = "task"
    SCHEDULE = "schedule"
    ARCHIVE = "archive"


@dataclass
class StoreEntry:
    key: str
    value: Any
    dimension: DimensionType
    namespace: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    version: int = 1
    tags: List[str] = field(default_factory=list)
    checksum: str = ""

    def __post_init__(self):
        self.checksum = self._compute_checksum()

    def _compute_checksum(self) -> str:
        raw = json.dumps({"key": self.key, "value": str(self.value), "dim": self.dimension}, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


class Store40D:
    """40-dimensional in-memory store with namespace isolation and thread safety."""

    DIMENSIONS = {d for d in DimensionType}

    def __init__(self, namespace: str = "default"):
        self.namespace = namespace
        self._store: Dict[str, Dict[str, StoreEntry]] = {d.value: {} for d in DimensionType}
        self._lock = threading.RLock()
        self._write_count = 0
        self._read_count = 0

    # ------------------------------------------------------------------
    # Core CRUD
    # ------------------------------------------------------------------

    def put(self, dimension: DimensionType, key: str, value: Any, tags: Optional[List[str]] = None) -> StoreEntry:
        with self._lock:
            existing = self._store[dimension.value].get(key)
            version = (existing.version + 1) if existing else 1
            entry = StoreEntry(
                key=key,
                value=value,
                dimension=dimension,
                namespace=self.namespace,
                version=version,
                tags=tags or [],
            )
            entry.updated_at = datetime.utcnow().isoformat()
            self._store[dimension.value][key] = entry
            self._write_count += 1
            return entry

    def get(self, dimension: DimensionType, key: str) -> Optional[Any]:
        with self._lock:
            self._read_count += 1
            entry = self._store[dimension.value].get(key)
            return entry.value if entry else None

    def delete(self, dimension: DimensionType, key: str) -> bool:
        with self._lock:
            if key in self._store[dimension.value]:
                del self._store[dimension.value][key]
                return True
            return False

    def query(self, dimension: DimensionType, tag: Optional[str] = None) -> List[StoreEntry]:
        with self._lock:
            entries = list(self._store[dimension.value].values())
            if tag:
                entries = [e for e in entries if tag in e.tags]
            return entries

    def search(self, key_prefix: str) -> Dict[str, List[StoreEntry]]:
        """Search across all 40 dimensions by key prefix."""
        results: Dict[str, List[StoreEntry]] = {}
        with self._lock:
            for dim_name, bucket in self._store.items():
                matches = [e for k, e in bucket.items() if k.startswith(key_prefix)]
                if matches:
                    results[dim_name] = matches
        return results

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------

    def get_metrics(self) -> Dict[str, Any]:
        with self._lock:
            counts = {dim: len(bucket) for dim, bucket in self._store.items()}
            total = sum(counts.values())
            return {
                "namespace": self.namespace,
                "total_entries": total,
                "dimensions_used": sum(1 for c in counts.values() if c > 0),
                "total_dimensions": len(DimensionType),
                "write_count": self._write_count,
                "read_count": self._read_count,
                "by_dimension": counts,
            }

    def export(self) -> Dict[str, Any]:
        with self._lock:
            return {
                dim: {
                    k: {
                        "value": e.value,
                        "version": e.version,
                        "tags": e.tags,
                        "checksum": e.checksum,
                        "updated_at": e.updated_at,
                    }
                    for k, e in bucket.items()
                }
                for dim, bucket in self._store.items()
            }


class Store40DFactory:
    @staticmethod
    def create_brand_store(namespace: str = "brand") -> Store40D:
        store = Store40D(namespace=namespace)
        store.put(DimensionType.CONFIG, "schema_version", "1.0", tags=["meta"])
        store.put(DimensionType.SIGNAL, "genesis", "SEEDWAVE-011-CORE", tags=["genesis", "immutable"])
        return store

    @staticmethod
    def create_build_store(namespace: str = "build") -> Store40D:
        store = Store40D(namespace=namespace)
        store.put(DimensionType.CONFIG, "build_engine", "MONSTER_OMNI", tags=["meta"])
        return store
