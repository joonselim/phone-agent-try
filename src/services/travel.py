from __future__ import annotations

from src.config import settings
from src.intent.schemas import ParsedIntent
from src.services.base import ServiceHandler


class YanoljaHandler(ServiceHandler):
    def get_package_name(self) -> str:
        return settings.yanolja_package

    def build_goal(self, intent: ParsedIntent) -> str:
        entities = intent.entities
        dest = entities.get("destination", "")
        dates = entities.get("dates", "")
        accom = entities.get("accommodation_type", "")
        num_guests = entities.get("num_guests", 1)

        search_term = dest or "accommodation"
        date_str = f" for {dates}" if dates else ""
        accom_str = f" {accom}" if accom else ""

        return (
            f"Open the Yanolja app and search for '{search_term}{accom_str}'{date_str}. "
            f"Set the number of guests to {num_guests} and only select items with free cancellation. "
            f"Complete the booking, then immediately cancel it for free from 'My Bookings'."
        )
