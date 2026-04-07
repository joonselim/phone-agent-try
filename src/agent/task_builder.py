from __future__ import annotations

from src.intent.schemas import ParsedIntent, ServiceCategory

SAFETY_SUFFIXES = {
    ServiceCategory.SHOPPING: "Complete the checkout. After the order is placed, immediately cancel it from 'Order History'.",
    ServiceCategory.DELIVERY: "Complete the checkout. After the order is placed, immediately cancel it from 'Orders' before cooking begins.",
    ServiceCategory.MOBILITY: "Complete the ride request. Immediately cancel it from 'Cancel Ride' whether or not a driver has been assigned.",
    ServiceCategory.TRAVEL: (
        "Only select items with free cancellation. After completing payment, immediately cancel for free from 'My Bookings'."
    ),
    ServiceCategory.RESERVATION: "Complete the reservation. After confirmation, immediately cancel it from 'My Reservations'.",
    ServiceCategory.GIFT: "Complete the gift send. Before the recipient opens it, immediately cancel from 'Gift History'.",
}


class TaskGoalBuilder:
    @staticmethod
    def build_goal(intent: ParsedIntent) -> str:
        suffix = SAFETY_SUFFIXES.get(intent.category, "")
        return f"{intent.minitap_goal} {suffix}".strip()
