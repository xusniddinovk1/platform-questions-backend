from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class IsAdminOrReadOnly(IsAuthenticated):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)
