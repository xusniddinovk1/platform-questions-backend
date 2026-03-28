from typing import Iterable

from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.auth.services.jwt import JWTService


class HasRole(BasePermission):
    """
    Проверяет, что пользователь имеет одну из разрешённых ролей.

    Можно задавать роли двумя способами:
    - через класс permission: `allowed_roles = (...)`
    - через view: `allowed_roles = (...)` (имеет приоритет)
    """

    allowed_roles: Iterable[str] = ()

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        auth_header = request.headers.get("Authorization")
        if not user or not user.is_authenticated:
            if not auth_header:
                raise NotAuthenticated("Authentication credentials were not provided.")
            raise AuthenticationFailed("Invalid or expired token")

        token_role: str | None = None
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()
            try:
                token_role = JWTService().decode_token(token).role
            except Exception:
                token_role = None

        effective_role = token_role or getattr(user, "role", None)

        view_allowed_roles = getattr(view, "allowed_roles", None)
        allowed_roles = view_allowed_roles or self.allowed_roles

        if not allowed_roles:
            return False

        return effective_role in allowed_roles
