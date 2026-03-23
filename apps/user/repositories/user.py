from django.db.models import QuerySet

from apps.auth.models import SocialAccount
from apps.user.models import User


class UserRepository:
    """
    Репозиторий для работы c пользователями.
    """

    def create(self, user: User) -> User:
        user.save()
        return user

    def list(self) -> QuerySet[User]:
        return User.objects.all()

    def get(self, id: int) -> User | None:
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def update(self, user: User) -> User:
        user.save()
        return user

    def delete(self, user: User) -> None:
        user.delete()

    def exists_email(self, email: str) -> bool:
        user = User.objects.filter(email=email).exists()
        return user

    def get_by_email(self, email: str) -> User | None:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_by_id(self, id: int) -> User | None:
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def exists_username(self, username: str) -> bool:
        return User.objects.filter(username=username).exists()

    def get_by_social(self, provider: str, provider_id: str) -> User | None:
        try:
            account = SocialAccount.objects.select_related("user").get(
                provider=provider, provider_id=provider_id
            )
            return account.user
        except SocialAccount.DoesNotExist:
            return None

    def create_social_account(
        self, user: User, provider: str, provider_id: str
    ) -> SocialAccount:
        return SocialAccount.objects.create(
            user=user, provider=provider, provider_id=provider_id
        )
