from typing import Iterable

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class HasRole(BasePermission):
    """
    Проверяет, что пользователь имеет одну из разрешённых ролей.
    """

    allowed_roles: Iterable[str] = ()

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.role in self.allowed_roles
