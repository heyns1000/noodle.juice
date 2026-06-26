"""
ClaimRoot™ (根契鎖定)
Oracle Bone Casting Foundation System

"One bone one pulse, one character one contract"
殿商卜骨 → 根契鴱造
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class ClaimType(Enum):
    BRAND = "brand"
    ASSET = "asset"
    LICENSE = "license"
    REPOSITORY = "repository"
    CONTRACT = "contract"
    CONTACT = "contact"


class ClaimStatus(Enum):
    PENDING = "pending"
    LOCKED = "locked"
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"


@dataclass
class OracleBone:
    """
    Oracle Bone (卜骨) - The foundation unit.
    Like ancient divination bones, each claim is inscribed and locked.
    """
    claim_id: str
    claim_type: ClaimType
    entity: str
    owner: str
    root_hash: str
    timestamp: float
    metadata: Dict[str, Any]
    status: ClaimStatus

    def to_dict(self) -> Dict:
        data = asdict(self)
        data['claim_type'] = self.claim_type.value
        data['status'] = self.status.value
        return data


class ClaimRoot:
    """
    ClaimRoot™ System
    Foundation locking mechanism that creates immutable roots for all entities.
    九天之契 (Nine Heaven Contract)
    """

    def __init__(self, storage_path: str = "./claimroot_store"):
        self.storage_path = storage_path
        self.bones: Dict[str, OracleBone] = {}
        self.root_chain: List[str] = []

    def cast_bone(self, claim_type: ClaimType, entity: str, owner: str, metadata: Optional[Dict] = None) -> OracleBone:
        timestamp = time.time()
        metadata = metadata or {}
        claim_id = self._generate_claim_id(entity, timestamp)
        root_hash = self._generate_root_hash(claim_id, claim_type.value, entity, owner, timestamp)
        bone = OracleBone(
            claim_id=claim_id, claim_type=claim_type, entity=entity, owner=owner,
            root_hash=root_hash, timestamp=timestamp, metadata=metadata, status=ClaimStatus.LOCKED,
        )
        self.bones[claim_id] = bone
        self.root_chain.append(root_hash)
        return bone

    def verify_bone(self, claim_id: str) -> bool:
        if claim_id not in self.bones:
            return False
        bone = self.bones[claim_id]
        calculated = self._generate_root_hash(bone.claim_id, bone.claim_type.value, bone.entity, bone.owner, bone.timestamp)
        return calculated == bone.root_hash

    def activate_bone(self, claim_id: str) -> bool:
        if claim_id not in self.bones:
            return False
        bone = self.bones[claim_id]
        if bone.status == ClaimStatus.LOCKED:
            bone.status = ClaimStatus.ACTIVE
            return True
        return False

    def query_bones(self, claim_type=None, owner=None, status=None) -> List[OracleBone]:
        results = list(self.bones.values())
        if claim_type:
            results = [b for b in results if b.claim_type == claim_type]
        if owner:
            results = [b for b in results if b.owner == owner]
        if status:
            results = [b for b in results if b.status == status]
        return results

    def get_bone(self, claim_id: str) -> Optional[OracleBone]:
        return self.bones.get(claim_id)

    def export_bones(self) -> Dict[str, Any]:
        return {
            "root_chain": self.root_chain,
            "total_bones": len(self.bones),
            "bones": [bone.to_dict() for bone in self.bones.values()],
            "export_timestamp": datetime.now().isoformat(),
        }

    def _generate_claim_id(self, entity: str, timestamp: float) -> str:
        return hashlib.sha256(f"{entity}_{timestamp}".encode()).hexdigest()[:16]

    def _generate_root_hash(self, claim_id, claim_type, entity, owner, timestamp) -> str:
        raw = f"{claim_id}:{claim_type}:{entity}:{owner}:{timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()


class ClaimRootFactory:
    @staticmethod
    def create_brand_claim(claimroot, brand_name, owner, sector, metadata=None):
        metadata = metadata or {}
        metadata['sector'] = sector
        return claimroot.cast_bone(ClaimType.BRAND, entity=brand_name, owner=owner, metadata=metadata)

    @staticmethod
    def create_license_claim(claimroot, license_id, owner, license_type, revenue_split, metadata=None):
        metadata = metadata or {}
        metadata['license_type'] = license_type
        metadata['revenue_split'] = revenue_split
        return claimroot.cast_bone(ClaimType.LICENSE, entity=license_id, owner=owner, metadata=metadata)

    @staticmethod
    def create_repo_claim(claimroot, repo_name, owner, github_url, metadata=None):
        metadata = metadata or {}
        metadata['github_url'] = github_url
        return claimroot.cast_bone(ClaimType.REPOSITORY, entity=repo_name, owner=owner, metadata=metadata)
