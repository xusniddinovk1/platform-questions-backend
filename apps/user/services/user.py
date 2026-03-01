from apps.auth.dto import RegisterRequestDTO
from apps.user.models import User
from apps.user.repositories.user import UserRepository


class UserService:
    """Сервис для работы c пользователями."""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def create_user(self, dto: RegisterRequestDTO) -> User:
        user = User(
            username=dto["username"],
            email=dto["email"],
            password=dto["password"],
            first_name=dto["first_name"],
            last_name=dto["last_name"],
            is_active=True,
            is_superuser=False,
            is_staff=False,
            birthday=dto["birthday"],
            university=dto["university"],
        )
        user.set_password(dto["password"])

        return self.user_repository.create(user)

    def is_user_exists(self, email: str) -> bool:
        is_exists = self.user_repository.exists_email(email=email)

        if is_exists:
            return True

        return False

    def get_user_by_email(self, email: str) -> User | None:
        return self.user_repository.get_by_email(email=email)

    def get_user_by_id(self, id: int) -> User | None:
        return self.user_repository.get_by_id(id=id)
