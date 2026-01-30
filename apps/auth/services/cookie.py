from rest_framework.response import Response

from apps.auth.config import (
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from apps.core.container import get_config_service
from apps.core.service import ConfigService


class CookieService:
    cookie_name: str
    config: ConfigService

    def __init__(self, cookie_name: str = "refresh_token") -> None:
        self.cookie_name = cookie_name
        self.config = get_config_service()

    def set_cookie(self, response: Response, token: str) -> Response:
        is_prod: bool = self.config.is_production()
        response.set_cookie(
            key=self.cookie_name,
            value=token,
            httponly=True,
            secure=is_prod,
            samesite="None" if is_prod else "Lax",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )
        return response

    def delete_cookie(self, response: Response) -> Response:
        response.delete_cookie(self.cookie_name)
        return response
