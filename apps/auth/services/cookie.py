from typing import Literal

from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.config import (
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from apps.core.service import ConfigService


class CookieService:
    cookie_name: str
    config: ConfigService

    def __init__(self, config: ConfigService, cookie_name: str = "refresh_token") -> None:
        self.cookie_name = cookie_name
        self.config = config

    def set_cookie(self, response: Response, token: str) -> Response:
        is_prod: bool = self.config.is_production()

        samesite: Literal["Lax", "Strict", "None", False]
        secure: bool

        if is_prod:
            samesite = "None"
            secure = True
        else:
            samesite = "Lax"
            secure = False

        response.set_cookie(
            key=self.cookie_name,
            value=token,
            httponly=True,
            secure=secure,
            samesite=samesite,
            path="/",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )
        return response

    def get_cookie(self, request: Request) -> str | None:
        return request.COOKIES.get(self.cookie_name)

    def delete_cookie(self, response: Response) -> Response:
        response.delete_cookie(key=self.cookie_name, path="/")
        return response
