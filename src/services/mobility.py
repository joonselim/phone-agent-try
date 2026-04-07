from __future__ import annotations

from src.config import settings
from src.intent.schemas import ParsedIntent
from src.services.base import ServiceHandler


class KakaoTHandler(ServiceHandler):
    def get_package_name(self) -> str:
        return settings.kakaot_package

    def build_goal(self, intent: ParsedIntent) -> str:
        entities = intent.entities
        dest = entities.get("destination", "destination")
        pickup_time = entities.get("pickup_time", "")
        time_str = f"at {pickup_time} " if pickup_time else ""
        return (
            f"Open the KakaoT app and request a taxi {time_str}to {dest}. "
            f"Once the ride is booked, immediately cancel it."
        )
