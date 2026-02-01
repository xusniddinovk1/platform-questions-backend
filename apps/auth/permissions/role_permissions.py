from apps.user.models import Role

from .role import HasRole


class IsAdmin(HasRole):
    allowed_roles = (Role.ADMIN,)


class IsUser(HasRole):
    allowed_roles = (Role.USER, Role.ADMIN)
