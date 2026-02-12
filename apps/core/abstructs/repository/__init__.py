from abc import ABC

from .read import ReadRepository
from .type import T
from .write import WriteRepository


class AbstractRepository(ReadRepository[T], WriteRepository[T], ABC):
    def __init__(self) -> None:
        pass
