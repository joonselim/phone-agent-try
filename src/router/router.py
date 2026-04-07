from src.config import settings
from src.intent.schemas import ParsedIntent, ServiceCategory

# Category → (app_key, package_name, display_name)
SERVICE_MAP = {
    ServiceCategory.SHOPPING: [
        ("coupang", settings.coupang_package, "Coupang"),
        ("naver_shopping", settings.naver_package, "Naver Shopping"),
    ],
    ServiceCategory.DELIVERY: [
        ("uber_eats", settings.uber_eats_package, "Uber Eats"),
        ("baemin", settings.baemin_package, "Baemin"),
        ("coupang_eats", settings.coupang_eats_package, "Coupang Eats"),
    ],
    ServiceCategory.MOBILITY: [
        ("kakaot", settings.kakaot_package, "KakaoT"),
    ],
    ServiceCategory.TRAVEL: [
        ("yanolja", settings.yanolja_package, "Yanolja"),
    ],
    ServiceCategory.RESERVATION: [
        ("catchtable", settings.catchtable_package, "Catchtable"),
        ("naver_reservation", settings.naver_package, "Naver Reservation"),
    ],
    ServiceCategory.GIFT: [
        ("kakao_gift", settings.kakao_package, "KakaoTalk Gift"),
    ],
}


class ServiceRouter:
    def route(self, intent: ParsedIntent) -> tuple[str, str, str]:
        """Resolve to (app_key, package_name, display_name) given an intent."""
        services = SERVICE_MAP.get(intent.category, [])
        if not services:
            raise ValueError(f"No service mapping for {intent.category}")

        # If user specified a preferred app, honor it
        if intent.app_preference:
            for app_key, package_name, name in services:
                if app_key == intent.app_preference:
                    intent.app_target = app_key
                    return (app_key, package_name, name)

        # Default to the first service in the category
        app_key, package_name, name = services[0]
        intent.app_target = app_key
        return (app_key, package_name, name)
