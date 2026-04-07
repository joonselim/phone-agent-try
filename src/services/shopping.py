from __future__ import annotations

from src.config import settings
from src.intent.schemas import ParsedIntent
from src.services.base import ServiceHandler


class CoupangHandler(ServiceHandler):
    def get_package_name(self) -> str:
        return settings.coupang_package

    def build_goal(self, intent: ParsedIntent) -> str:
        entities = intent.entities
        product = entities.get("product", "item")

        if entities.get("use_previous_order"):
            return (
                f"Open the Coupang app, go to 'My Coupang' → 'Order History', "
                f"find the most recent order of {product}, and tap 'Reorder'. "
                f"Complete checkout. After the order is placed, immediately cancel it from 'Order History'."
            )

        brand = entities.get("brand", "")
        quantity = entities.get("quantity", 1)
        return (
            f"Open the Coupang app and search for '{brand} {product}' in the search bar. "
            f"Select a highly rated Rocket Delivery item, set quantity to {quantity}, and complete checkout. "
            f"After the order is placed, immediately cancel it from 'Order History'."
        )


class NaverShoppingHandler(ServiceHandler):
    def get_package_name(self) -> str:
        return settings.naver_package

    def build_goal(self, intent: ParsedIntent) -> str:
        entities = intent.entities
        product = entities.get("product", "item")
        return (
            f"Open the Naver app and search for '{product}'. "
            f"Go to the 'Shopping' tab, select a reasonably priced item, and complete checkout. "
            f"After the order is placed, immediately cancel it from 'Order History'."
        )
