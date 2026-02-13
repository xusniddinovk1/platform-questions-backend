from abc import abstractmethod
from typing import Optional

from apps.core.abstructs.repository import AbstractRepository
from apps.core.abstructs.repository.read import ReadRepository
from apps.core.abstructs.repository.write import WriteRepository


class User:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name


class UserRepository(AbstractRepository[User]):
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def add(self, entity: User) -> None:
        pass


class UserOnlyReadRepository(ReadRepository[User]):
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[User]:
        pass


class UserOnlyWriteRepository(WriteRepository[User]):
    @abstractmethod
    def add(self, entity: User) -> None:
        pass
