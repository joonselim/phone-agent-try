from __future__ import annotations

from src.agent.droid_agent import DroidRunAgent
from src.intent.parser import IntentParser
from src.intent.schemas import ParsedIntent, ServiceAction, ServiceCategory
from src.router.router import ServiceRouter
from src.services.base import ServiceHandler
from src.state.conversation import ConversationManager

# Restaurants that can be ordered directly on Uber Eats without Claude API call
UBER_EATS_FAST_KEYWORDS: dict[str, str] = {
    "kfc": "KFC",
    "mcdonald": "McDonald's",
    "mcdonalds": "McDonald's",
    "burger king": "Burger King",
    "subway": "Subway",
    "domino": "Domino's",
    "pizza hut": "Pizza Hut",
    "starbucks": "Starbucks",
    "chick-fil-a": "Chick-fil-A",
    "chickfila": "Chick-fil-A",
    "taco bell": "Taco Bell",
    "wendy": "Wendy's",
}


def _fast_uber_eats_intent(restaurant: str) -> ParsedIntent:
    return ParsedIntent(
        category=ServiceCategory.DELIVERY,
        action=ServiceAction.ORDER,
        entities={"restaurant": restaurant},
        app_preference="uber_eats",
        app_target="uber_eats",
        minitap_goal="",
        needs_clarification=False,
        confidence=1.0,
    )


class CLIApp:
    def __init__(
        self,
        parser: IntentParser,
        router: ServiceRouter,
        agent: DroidRunAgent,
        handlers: dict[str, ServiceHandler],
    ) -> None:
        self.parser = parser
        self.router = router
        self.agent = agent
        self.handlers = handlers
        self.conversation = ConversationManager()
        self.user_id = 0

    async def run(self) -> None:
        print("=" * 60)
        print("Android agent try- automating on a physical phone via Droidrun ")
        print("=" * 60)
        print("To quit: 'quit' or 'exit'\n")
        print("Examples:")
        print("  • Order more shampoo")
        print("  • Recommend something for dinner tonight and order it")
        print("  • Buy anything that I would like from Amazon")
        print("-" * 60)

        while True:
            try:
                user_input = input("\n💬 You: ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if user_input.lower() in ("quit", "exit", "종료"):
                print("Goodbye.")
                break
            if not user_input:
                continue

            self.conversation.add_message(self.user_id, "user", user_input)

            # Fast path: skip Claude API if a known restaurant keyword is detected
            lowered = user_input.lower()
            fast_restaurant = next(
                (name for kw, name in UBER_EATS_FAST_KEYWORDS.items() if kw in lowered), None
            )
            if fast_restaurant:
                print(f"Fast path: ordering from {fast_restaurant} on Uber Eats...")
                intent = _fast_uber_eats_intent(fast_restaurant)
            else:
                ctx = self.conversation.get_context_for_parser(self.user_id)
                print("Analyzing...")
                try:
                    intent = await self.parser.parse(user_input, context=ctx)
                except Exception as e:
                    print(f"Error: Failed to parse intent: {e}")
                    continue

            if intent.needs_clarification:
                self.conversation.set_pending_intent(self.user_id, intent)
                print(f"Question: {intent.clarification_question}")
                self.conversation.add_message(self.user_id, "assistant", intent.clarification_question or "")
                continue

            app_key, package_name, display_name = self.router.route(intent)
            print(f"Handling with {display_name}...")
            print(f"   Category: {intent.category.value}")
            print(f"   Action: {intent.action.value}")
            print(f"   App: {display_name} ({package_name})")

            handler = self.handlers.get(app_key)
            if not handler:
                print(f"Error: No handler implemented for {display_name}.")
                continue

            try:
                result = await handler.execute(intent)
                if result.get("success"):
                    print(f"Done: {display_name} completed successfully.")
                    if result.get("screenshot"):
                        print(f"Screenshot: {result['screenshot']}")
                    if result.get("trace_path"):
                        print(f"Trace: {result['trace_path']}")
                    self.conversation.add_message(self.user_id, "assistant", f"{display_name} completed")
                else:
                    print(f"Failed: {display_name} error: {result.get('error', 'Unknown error')}")
                    if result.get("trace_path"):
                        print(f"Trace: {result['trace_path']}")
            except Exception as e:
                print(f"Error during execution: {e}")
