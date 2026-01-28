from typing import override

from apps.notifications.abstructs import NotificationSender


class SMSSender(NotificationSender):
    @override
    def send(self, to: str, message: str) -> None:
        print(f"Sending SMS to {to}: {message}")
