from typing import override

from django.conf import settings
from django.core.mail import send_mail

from apps.notifications.abstructs import NotificationSender


class EmailSenderService(NotificationSender):
    @override
    def send(self, to: str, subject: str, message: str) -> None:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to],
            fail_silently=False,
        )


# def send_confirmation_email(request, user):
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)

#     confirm_url = f"http://localhost:8000/auth/confirm/{uid}/{token}/"

#     send_mail(
#         subject="Подтверждение регистрации",
#         message=f"Перейдите по ссылке для подтверждения:\n{confirm_url}",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[user.email],
#         fail_silently=False,
#     )
