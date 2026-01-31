from __future__ import annotations

from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.request import Request


class IsAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request: Request, view: object) -> bool:
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        # mypy union-attr muammosini ham yopadi:
        return bool(getattr(request.user, "is_staff", False))


__all__ = ["IsAdminOrReadOnly", "IsAuthenticated"]
