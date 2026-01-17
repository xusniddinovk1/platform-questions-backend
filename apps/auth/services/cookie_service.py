from rest_framework.response import Response

from apps.auth.config import (
    REFRESH_TOKEN_EXPIRE_DAYS,
)


class CookieService:
    COOKIE_NAME: str

    def __init__(self, cookie_name: str = "refresh_token") -> None:
        self.COOKIE_NAME = cookie_name

    def set_cookie(self, response: Response, token: str) -> Response:
        response.set_cookie(
            key=self.COOKIE_NAME,
            value=token,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )
        return response

    def delete_cookie(self, response: Response) -> Response:
        response.delete_cookie(self.COOKIE_NAME)
        return response
