from apps.user.models import Role

from .role import HasRole


class IsAuthenticatedUser(HasRole):
    allowed_roles = (Role.ADMIN, Role.USER)


class IsAdmin(HasRole):
    allowed_roles = (Role.ADMIN,)


class IsUser(HasRole):
    allowed_roles = (Role.USER, Role.ADMIN)


class IsOnlyUser(HasRole):
    allowed_roles = (Role.USER,)


class IsAdminOrUser(HasRole):
    allowed_roles = (Role.ADMIN, Role.USER)
