from __future__ import annotations

from src.config import settings
from src.intent.schemas import ParsedIntent
from src.services.base import ServiceHandler


class KakaoGiftHandler(ServiceHandler):
    def get_package_name(self) -> str:
        return settings.kakao_package

    def build_goal(self, intent: ParsedIntent) -> str:
        entities = intent.entities
        recipient = entities.get("recipient", "the recipient")
        item_type = entities.get("item_type", "")
        budget = entities.get("budget", "")
        occasion = entities.get("occasion", "")

        item_str = item_type or "popular gift"
        budget_str = f" within {budget}" if budget else ""
        occasion_str = f" ({occasion})" if occasion else ""

        return (
            f"Open the KakaoTalk app, go to the 'More' tab at the bottom, then 'Gift'. "
            f"Search for '{item_str}' and select an appropriate item{budget_str}. "
            f"Complete sending the gift to '{recipient}'{occasion_str}. "
            f"Before the recipient opens it, immediately cancel from 'Gift History'."
        )
