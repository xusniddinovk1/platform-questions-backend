from django.db.models import QuerySet

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
        return User.objects.get(id=id)

    def update(self, user: User) -> User:
        user.save()
        return user

    def delete(self, user: User) -> None:
        user.delete()

    def exists_email(self, email: str) -> bool:
        user = User.objects.filter(email=email).exists()
        return user

    def get_by_email(self, email: str) -> User | None:
        return User.objects.get(email=email)
