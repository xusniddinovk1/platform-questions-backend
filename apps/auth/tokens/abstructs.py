from abc import ABC, abstractmethod

from apps.user.models import User


class TokenGenerator(ABC):
    @abstractmethod
    def make(self, user: User) -> str: ...

    @abstractmethod
    def check_token(self, user: User, token: str) -> bool: ...
