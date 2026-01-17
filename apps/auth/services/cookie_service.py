from rest_framework.response import Response

from apps.auth.config import (
    REFRESH_TOKEN_EXPIRE_DAYS,
)


class CookieService:
    cookie_name: str

    def __init__(self, cookie_name: str = "refresh_token") -> None:
        self.cookie_name = cookie_name

    def set_cookie(self, response: Response, token: str) -> Response:
        response.set_cookie(
            key=self.cookie_name,
            value=token,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )
        return response

    def delete_cookie(self, response: Response) -> Response:
        response.delete_cookie(self.cookie_name)
        return response
