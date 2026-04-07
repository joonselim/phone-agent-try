SYSTEM_PROMPT = """You are an expert intent classifier for local services.
Analyze the user's input and extract the service category, action, and entities.

Categories:
- shopping: Shopping/purchasing (Coupang, Naver Shopping)
- delivery: Food delivery (Baemin, Coupang Eats, Uber Eats). Use this for anything hunger-related: "I'm hungry", "order me food", "get me something to eat", etc.
- mobility: Transportation (KakaoT)
- travel: Travel/accommodation (Yanolja)
- reservation: Restaurant reservation (Catchtable, Naver Reservation)
- gift: Gift sending (KakaoTalk Gift)

Rules:
1. Understand both formal and informal speech, in any language
2. "The one I ordered last time" = use_previous_order: true
3. Only set needs_clarification: true if the request is completely unactionable (e.g. no category can be determined at all). If a restaurant name OR food type is mentioned, never ask for clarification — just proceed.
4. minitap_goal should describe the task to perform in the app in natural language, in detail
5. If the user specifies an app, set app_preference to the corresponding key:
   - "Coupang" → coupang, "Naver Shopping / on Naver" → naver_shopping
   - "Baemin / Baedal Minjok" → baemin, "Coupang Eats" → coupang_eats
   - "Uber Eats / UberEats" → uber_eats
   - "KakaoT / Kakao Taxi" → kakaot, "Yanolja" → yanolja
   - "Catchtable" → catchtable, "Naver Reservation / on Naver" → naver_reservation
   - "KakaoTalk Gift" → kakao_gift
6. If no app is specified, app_preference is null (router will choose the default)

Entity extraction guide (required fields per category):
- shopping: product(required), brand, quantity, price_range, use_previous_order
- delivery: cuisine(food type), restaurant(restaurant name), price_range, solo_or_group, time
- mobility: destination(required), pickup_time, vehicle_type
- travel: destination(required), dates, accommodation_type, budget, num_guests
- reservation: cuisine(e.g. Western/Korean/Japanese/Chinese), venue_name(specific restaurant),
  location(area), party_size, reservation_date(e.g. "April 4"), reservation_time(e.g. "6pm")
- gift: recipient(required), occasion, item_type, budget, delivery_address

Reservation entity notes:
- Always extract cuisine type (Western, Korean, Japanese, etc.) into the cuisine field
- Split date and time into reservation_date and reservation_time separately
- "with my girlfriend" = party_size: 2, "4 of us" = party_size: 4
"""

PARSE_INTENT_TOOL = {
    "name": "parse_intent",
    "description": "Parse intent from the user's utterance",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["shopping", "delivery", "mobility", "travel", "reservation", "gift"],
            },
            "action": {
                "type": "string",
                "enum": ["order", "search", "book", "reserve", "cancel", "compare", "recommend"],
            },
            "entities": {
                "type": "object",
                "description": (
                    "Entities per category. "
                    "reservation: {cuisine, venue_name, location, party_size, reservation_date, reservation_time}. "
                    "delivery: {cuisine, restaurant, price_range, solo_or_group, time}. "
                    "shopping: {product, brand, quantity, price_range, use_previous_order}. "
                    "mobility: {destination, pickup_time, vehicle_type}. "
                    "travel: {destination, dates, accommodation_type, budget, num_guests}. "
                    "gift: {recipient, occasion, item_type, budget, delivery_address}."
                ),
            },
            "minitap_goal": {
                "type": "string",
                "description": "Natural language goal to pass to the agent (detailed)",
            },
            "app_preference": {
                "type": ["string", "null"],
                "description": (
                    "App key if the user specified a particular app. E.g.: coupang, naver_shopping, baemin, coupang_eats, "
                    "uber_eats, kakaot, yanolja, catchtable, naver_reservation, kakao_gift. Null if not specified."
                ),
                "enum": [
                    "coupang",
                    "naver_shopping",
                    "baemin",
                    "coupang_eats",
                    "uber_eats",
                    "kakaot",
                    "yanolja",
                    "catchtable",
                    "naver_reservation",
                    "kakao_gift",
                    None,
                ],
            },
            "needs_clarification": {"type": "boolean"},
            "clarification_question": {"type": ["string", "null"]},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        },
        "required": ["category", "action", "entities", "minitap_goal", "needs_clarification", "confidence"],
    },
}
