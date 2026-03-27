from typing import Optional, Tuple

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from apps.auth.container import get_auth_service
from apps.user.models import User

auth_service = get_auth_service()


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[User, None]]:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        token: str | None = None
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()
        else:
            candidate = auth_header.strip()
            if candidate.count(".") == 2:
                token = candidate

        if not token:
            return None

        try:
            user = auth_service.authenticate_token(token)
        except ValueError:
            raise AuthenticationFailed("Invalid or expired token")

        if user is None:
            return None

        return (user, None)
