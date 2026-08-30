"""
BareCart™ — Grain-level commerce layer
1 grain = $0.01 USD | Zero surprises pricing
"""
import hashlib, time
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum


class ItemType(Enum):
    LICENSE = "license"
    BRAND = "brand"
    SERVICE = "service"
    ASSET = "asset"


@dataclass
class CartItem:
    name: str
    item_type: ItemType
    price: float
    quantity: int = 1


@dataclass
class Cart:
    cart_id: str
    owner: str
    items: List[CartItem] = field(default_factory=list)
    status: str = "open"
    total: float = 0.0


class BareCart:
    def __init__(self):
        self.carts: Dict[str, Cart] = {}
        self._revenue: float = 0.0

    def finalize_cart(self, cart_id: str):
        if cart_id in self.carts:
            self.carts[cart_id].status = "finalized"

    def process_cart(self, cart_id: str) -> Dict[str, Any]:
        if cart_id not in self.carts:
            return {"error": "cart not found"}
        cart = self.carts[cart_id]
        total = sum(i.price * i.quantity for i in cart.items) or cart.total
        cart.total = total
        cart.status = "processed"
        self._revenue += total
        return {"cart_id": cart_id, "total_price": total, "status": cart.status}

    def get_metrics(self) -> Dict[str, Any]:
        return {"total_carts": len(self.carts), "total_revenue": self._revenue}

    def export_carts(self) -> Dict[str, Any]:
        return {"carts": [{"cart_id": c.cart_id, "owner": c.owner, "total": c.total} for c in self.carts.values()]}


class BareCartFactory:
    @staticmethod
    def create_license_cart(barecart, owner, license_type, duration_months, monthly_price) -> Cart:
        cart_id = hashlib.sha256(f"{owner}{time.time()}".encode()).hexdigest()[:16]
        cart = Cart(
            cart_id=cart_id, owner=owner,
            items=[CartItem(name=f"{license_type} x{duration_months}mo", item_type=ItemType.LICENSE, price=monthly_price, quantity=duration_months)],
            total=monthly_price * duration_months,
        )
        barecart.carts[cart_id] = cart
        return cart
