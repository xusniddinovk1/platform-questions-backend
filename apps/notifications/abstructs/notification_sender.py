from abc import ABC, abstractmethod


class NotificationSender(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, message: str) -> None:
        pass
