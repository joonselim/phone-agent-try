from __future__ import annotations

from src.config import settings
from src.intent.schemas import ParsedIntent
from src.services.base import ServiceHandler


class CatchtableHandler(ServiceHandler):
    def get_package_name(self) -> str:
        return settings.catchtable_package

    def build_goal(self, intent: ParsedIntent) -> str:
        entities = intent.entities
        venue = entities.get("venue_name", "")
        cuisine = entities.get("cuisine", "")
        service_type = entities.get("service_type", "")
        party_size = entities.get("party_size", 2)
        date = entities.get("reservation_date", "")
        time = entities.get("reservation_time", "")

        if venue:
            search = venue
        elif cuisine:
            search = f"{cuisine} restaurant"
        elif service_type:
            search = service_type
        else:
            search = "restaurant"

        instructions: list[str] = []
        instructions.append(f"Open the Catchtable app and search for '{search}'.")
        instructions.append("Select an available restaurant.")

        if date:
            instructions.append(f"Set the date to {date}.")
        if time:
            instructions.append(f"Set the time to {time}.")

        instructions.append(f"Set the party size to {party_size}.")
        instructions.append("Fill in the reservation form and complete the booking.")
        instructions.append("After confirmation, immediately cancel it from 'My Reservations'.")

        return " ".join(instructions)


class NaverReservationHandler(ServiceHandler):
    def get_package_name(self) -> str:
        return settings.naver_package

    def build_goal(self, intent: ParsedIntent) -> str:
        entities = intent.entities
        venue = entities.get("venue_name", "")
        cuisine = entities.get("cuisine", "")
        service_type = entities.get("service_type", "")
        location = entities.get("location", "")
        party_size = entities.get("party_size", 2)
        date = entities.get("reservation_date", "")
        time = entities.get("reservation_time", "")

        if venue:
            search = venue
        elif cuisine and location:
            search = f"{location} {cuisine}"
        elif cuisine:
            search = f"{cuisine} restaurant"
        elif service_type:
            search = service_type
        else:
            search = "restaurant"

        if location and location not in search:
            search = f"{location} {search}"

        instructions: list[str] = []
        instructions.append(f"Open the Naver app and search for '{search}'.")
        instructions.append("Select a place that has a 'Reserve' button.")

        if date:
            instructions.append(f"Set the date to {date}.")
        if time:
            instructions.append(f"Set the time to {time}.")

        instructions.append(f"Complete the reservation for {party_size} people.")
        instructions.append("After confirmation, immediately cancel it from 'My Reservations'.")

        return " ".join(instructions)
