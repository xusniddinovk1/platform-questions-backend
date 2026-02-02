from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.auth.tokens.abstructs import TokenGenerator
from apps.user.models import User


class ConfirmationLinkService:
    def __init__(self, token_generator: TokenGenerator) -> None:
        self.token_generator = token_generator

    def build(self, user: User) -> str:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = self.token_generator.make(user)

        path = reverse(
            "confirm_email",
            kwargs={"uidb64": uid, "token": token},
        )

        return f"{settings.SITE_URL}{path}"
