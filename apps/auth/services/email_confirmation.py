from django.utils.http import urlsafe_base64_decode

from apps.auth.tokens.abstructs import TokenGenerator
from apps.core.logger import LoggerType
from apps.notifications.abstructs import NotificationSender
from apps.user.models import User

from .confirmation_link import ConfirmationLinkService


class EmailConfirmationService:
    def __init__(
        self,
        sender: NotificationSender,
        link_service: ConfirmationLinkService,
        log: LoggerType,
    ) -> None:
        self.sender = sender
        self.link_service = link_service
        self.log = log

    def send_confirmation(self, user: User) -> None:
        confirm_url = self.link_service.build(user)

        self.log.info(
            f"Sending confirmation email user_id={user.id} email={user.email}",
        )

        self.sender.send(
            to=user.email,
            subject="Подтверждение регистрации",
            message=(f"Перейдите по ссылке для подтверждения:\n{confirm_url}"),
        )

        self.log.debug(confirm_url)


class EmailConfirmationActivationService:
    def __init__(self, token_generator: TokenGenerator) -> None:
        self.token_generator = token_generator

    def confirm(self, uidb64: str, token: str) -> bool:
        """
        Возвращает:
        - True  -> email успешно подтверждён
        - False -> токен невалиден / пользователь не найден
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return False

        if not self.token_generator.check_token(user, token):
            return False

        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])

        return True
