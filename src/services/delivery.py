from __future__ import annotations

from src.config import settings
from src.intent.schemas import ParsedIntent
from src.services.base import ServiceHandler


class BaeminHandler(ServiceHandler):
    def get_package_name(self) -> str:
        return settings.baemin_package

    def build_goal(self, intent: ParsedIntent) -> str:
        entities = intent.entities
        cuisine = entities.get("cuisine", "")
        restaurant = entities.get("restaurant", "")

        if restaurant:
            return (
                f"Open the Baemin app and search for '{restaurant}' in the search bar. "
                f"Select a menu item, add it to the cart, and complete checkout. "
                f"After the order is placed, immediately cancel it from 'Orders' before cooking begins."
            )

        return (
            f"Open the Baemin app and browse {f'the {cuisine} category' if cuisine else 'recommended restaurants'}. "
            f"Pick a highly rated restaurant, select a menu item, add it to the cart, and complete checkout. "
            f"After the order is placed, immediately cancel it from 'Orders' before cooking begins."
        )


class CoupangEatsHandler(ServiceHandler):
    def get_package_name(self) -> str:
        return settings.coupang_eats_package

    def build_goal(self, intent: ParsedIntent) -> str:
        entities = intent.entities
        cuisine = entities.get("cuisine", "")
        restaurant = entities.get("restaurant", "")

        if restaurant:
            return (
                f"Open the Coupang Eats app and search for '{restaurant}' in the search bar. "
                f"Select a menu item, add it to the cart, and complete checkout. "
                f"After the order is placed, immediately cancel it from 'Orders' before cooking begins."
            )

        return (
            f"Open the Coupang Eats app and browse {f'the {cuisine} category' if cuisine else 'recommended restaurants'}. "
            f"Pick a highly rated restaurant, select a menu item, add it to the cart, and complete checkout. "
            f"After the order is placed, immediately cancel it from 'Orders' before cooking begins."
        )


class UberEatsHandler(ServiceHandler):
    def get_package_name(self) -> str:
        return settings.uber_eats_package

    def get_goal(self, intent: ParsedIntent) -> str:
        """Override to always use a fast, direct goal — skip minitap_goal."""
        from src.memory import user_memory

        ctx = user_memory.get_context_for_goal(intent.category)
        core = self.build_goal(intent)
        return f"{ctx}{core}".strip()

    def build_goal(self, intent: ParsedIntent) -> str:
        entities = intent.entities
        restaurant = entities.get("restaurant", "")

        if restaurant:
            return (
                f"Uber Eats app is already open. "
                f"Step 1: If any popup or modal is visible, dismiss it immediately (tap X, 'No thanks', or 'Close'). Do not scroll or explore. "
                f"Step 2: Tap '{restaurant}' on the home screen. Do NOT search. "
                f"Step 3: Tap the very first menu item visible. Do NOT scroll down. "
                f"Step 4: As soon as an 'Add to cart' or 'Add' button appears, tap it immediately. "
                f"Step 5: Tap 'Checkout' or 'Place order' the moment it appears. Do not scroll, do not review, do not wait. "
                f"Step 6: After the order is placed, cancel it from 'Orders'."
            )

        return (
            "Uber Eats app is already open. "
            "Tap the very first restaurant or food item visible on the screen right now — no searching, no scrolling. "
            "Inside the restaurant, tap the very first menu item you see and add exactly 1 to the cart. "
            "Go straight to checkout and place the order immediately. "
            "After the order is placed, cancel it from 'Orders'."
        )
