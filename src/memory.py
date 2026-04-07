from __future__ import annotations

import re
from pathlib import Path

from src.intent.schemas import ServiceCategory


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


class UserMemory:
    """Loads `memory.md` from the project root for agent personalization."""

    def __init__(self, memory_path: Path | None = None) -> None:
        self._path = memory_path or (_project_root() / "memory.md")
        self._raw: str = ""
        self.reload()

    def reload(self) -> None:
        if self._path.is_file():
            self._raw = self._path.read_text(encoding="utf-8").strip()
        else:
            self._raw = ""

    def _extract(self, key: str) -> str:
        """Extract the value of `- **key**: value` from the raw markdown."""
        for line in self._raw.splitlines():
            m = re.match(rf"^-\s+\*\*{re.escape(key)}\*\*:\s*(.+)", line.strip())
            if m:
                return m.group(1).strip()
        return ""

    def get_profile_prompt(self) -> str:
        """Append to intent parser system prompt so Claude knows the user."""
        if not self._raw:
            return ""
        return (
            "\n\n[User Profile — apply the following when interpreting intent, making recommendations, and extracting entities]\n"
            f"{self._raw}\n"
            "[End User Profile]\n"
        )

    def get_context_for_goal(self, category: ServiceCategory) -> str:
        """Compact, category-relevant context for Droid agent goals.

        Only includes fields the Droid agent actually needs for the given
        category so the goal string stays short and focused.
        """
        if not self._raw:
            return ""

        name = self._extract("name")
        phone = self._extract("phone")
        home = self._extract("home_address")
        work = self._extract("work_address")
        likes = self._extract("food_preferences")
        dislikes = self._extract("food_dislikes")
        gf_pref = self._extract("partner_food_preferences")

        blocks: dict[ServiceCategory, str] = {
            ServiceCategory.DELIVERY: (
                f"Delivery address: {home}. "
                f"Likes: {likes}. Dislikes: {dislikes}. "
                f"When with partner: {gf_pref}."
            ),
            ServiceCategory.MOBILITY: (
                f"Home: {home}. Work: {work}. "
                f"Name: {name}. Phone: {phone}."
            ),
            ServiceCategory.RESERVATION: (
                f"Likes: {likes}. Dislikes: {dislikes}. "
                f"When with partner: {gf_pref}."
            ),
            ServiceCategory.SHOPPING: (
                f"Shipping address: {home}. "
                f"Name: {name}. Phone: {phone}."
            ),
            ServiceCategory.TRAVEL: f"Booker: {name}. Contact: {phone}.",
            ServiceCategory.GIFT: f"Sender: {name}. Contact: {phone}.",
        }
        ctx = blocks.get(category)
        if not ctx:
            return ""
        return f"[User Info] {ctx}\n"


user_memory = UserMemory()
