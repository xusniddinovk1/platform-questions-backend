from apps.auth.dto import RegisterRequestDTO
from apps.auth.dto.google_oauth import GoogleUserInfoDTO
from apps.auth.models import AuthProvider
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
            is_active=False,
            is_superuser=False,
            is_staff=False,
            birthday=dto["birthday"],
            university="",
        )
        user.set_password(dto["password"])

        return self.user_repository.create(user)

    # def create_google_user(self, info: GoogleUserInfoDTO) -> User:
    #     """Create a new user from Google profile data."""
    #     base_username = info["email"].split("@")[0]
    #     username = self._unique_username(base_username)

    #     user = User(
    #         username=username,
    #         email=info["email"],
    #         first_name=info["given_name"],
    #         last_name=info["family_name"],
    #         google_id=info["sub"],
    #         auth_provider=AuthProvider.GOOGLE,
    #         is_active=True,
    #         is_superuser=False,
    #         is_staff=False,
    #     )
    #     user.set_unusable_password()
    #     return self.user_repository.create(user)

    def create_google_user(self, info: GoogleUserInfoDTO) -> User:
        base_username = info["email"].split("@")[0]
        username = self._unique_username(base_username)

        user = User(
            username=username,
            email=info["email"],
            first_name=info["given_name"],
            last_name=info["family_name"],
            is_active=True,
            is_superuser=False,
            is_staff=False,
        )
        user.set_unusable_password()
        user = self.user_repository.create(user)

        # Создаём связанный SocialAccount
        self.user_repository.create_social_account(
            user=user,
            provider=AuthProvider.GOOGLE,
            provider_id=info["sub"],
        )
        return user

    def _unique_username(self, base: str) -> str:
        candidate = base
        counter = 1
        while self.user_repository.exists_username(candidate):
            candidate = f"{base}{counter}"
            counter += 1
        return candidate

    # def get_user_by_google_id(self, google_id: str) -> User | None:
    #     return self.user_repository.get_by_google_id(google_id)
    def get_user_by_social(self, provider: str, provider_id: str) -> User | None:
        return self.user_repository.get_by_social(
            provider=provider, provider_id=provider_id
        )

    def is_user_exists(self, email: str) -> bool:
        is_exists = self.user_repository.exists_email(email=email)

        if is_exists:
            return True

        return False

    def get_user_by_email(self, email: str) -> User | None:
        return self.user_repository.get_by_email(email=email)

    def get_user_by_id(self, id: int) -> User | None:
        return self.user_repository.get_by_id(id=id)

    def update_user(self, user: User) -> User:
        """
        Обновление существующего пользователя.
        """
        return self.user_repository.update(user)
