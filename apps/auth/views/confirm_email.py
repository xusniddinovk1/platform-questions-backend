# from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.auth.container import get_confirmation_activation_service
from apps.auth.services.email_confirmation import EmailConfirmationActivationService
from apps.auth.swagger.confirm_email import email_confirm_swagger
from apps.core.container import get_config_service
from apps.core.service import ConfigService


class EmailConfirmAPIView(APIView):
    """
    API endpoint для подтверждения email по ссылке.
    URL: /v1/auth/confirm/<uidb64>/<token>/
    """

    config: ConfigService
    activation_service: EmailConfirmationActivationService

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)
        self.config = get_config_service()
        self.activation_service = get_confirmation_activation_service()

    @email_confirm_swagger
    def get(self, request: Request, uidb64: str, token: str) -> HttpResponseRedirect:
        success = self.activation_service.confirm(uidb64, token)

        FRONTEND_URL = self.config.settings.FRONTEND_URL

        if success:
            return HttpResponseRedirect(f"{FRONTEND_URL}/email-confirm?status=success")
        else:
            return HttpResponseRedirect(f"{FRONTEND_URL}/email-confirm?status=invalid")
