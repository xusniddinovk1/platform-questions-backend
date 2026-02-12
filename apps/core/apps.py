from django.apps import AppConfig

from apps.core.container import get_config_service
from apps.core.logger import get_logger_service

log = get_logger_service(__name__)
config_service = get_config_service()


class CoreConfig(AppConfig):
    name = "apps.core"

    def ready(self) -> None:
        log.info(
            "Application started | state=%s | swagger=%s",
            config_service.state_app,
            config_service.url_swagger(),
        )
