from typing import Optional, Tuple

from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from apps.auth.container import get_auth_service
from apps.user.models import User

auth_service = get_auth_service()


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[User, None]]:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        user = auth_service.authenticate_token(token)

        if user is None:
            return None

        return (user, None)
