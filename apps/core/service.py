import os

from django.conf import settings


class ConfigService:
    """
    Сервис для работы c конфигурацией приложения.
    """

    state_app: str  # dev | prod

    def __init__(self) -> None:
        self.state_app = os.getenv("DJANGO_ENV", "dev")
        self.settings = settings

    def is_production(self) -> bool:
        return self.state_app == "prod"

    def url_swagger(self) -> str:
        return getattr(self.settings, "SWAGGER_URL", "/docs/")
