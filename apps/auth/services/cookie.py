import os

from rest_framework.response import Response

from apps.auth.config import (
    REFRESH_TOKEN_EXPIRE_DAYS,
)

DJANGO_ENV = os.getenv("DJANGO_ENV", "dev")
IS_PROD = DJANGO_ENV == "prod"


class CookieService:
    cookie_name: str

    def __init__(self, cookie_name: str = "refresh_token") -> None:
        self.cookie_name = cookie_name

    def set_cookie(self, response: Response, token: str) -> Response:
        response.set_cookie(
            key=self.cookie_name,
            value=token,
            httponly=True,
            secure=IS_PROD,
            samesite="None" if IS_PROD else "Lax",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )
        return response

    def delete_cookie(self, response: Response) -> Response:
        response.delete_cookie(self.cookie_name)
        return response
