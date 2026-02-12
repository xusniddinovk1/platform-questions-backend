from abc import ABC, abstractmethod
from typing import Generic, List, Optional

from .type import T


class ReadRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass
