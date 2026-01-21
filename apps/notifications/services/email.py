from typing import override

from apps.notifications.abstructs import NotificationSender


class EmailSender(NotificationSender):
    @override
    def send(self, to: str, message: str) -> None:
        print(f"Sending Email to {to}: {message}")
