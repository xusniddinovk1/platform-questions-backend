from apps.user.repositories.user import UserRepository
from apps.user.services.user import UserService


def get_user_service() -> UserService:
    repo = UserRepository()
    svc = UserService(repo)
    return svc
