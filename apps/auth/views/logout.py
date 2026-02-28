from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.container import get_auth_service, get_cookie_service
from apps.auth.serializers.logout import LogoutSerializer
from apps.auth.services.auth import AuthService
from apps.auth.services.cookie import CookieService
from apps.auth.swagger.logout import logout_swagger
from apps.core.logger import LoggerType, get_logger_service
from apps.core.responses import build_success_response


class LogoutView(APIView):
    """
    post:
    Выход из системы.
    """

    cookie_service: CookieService
    auth_service: AuthService
    log: LoggerType

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)
        self.auth_service = get_auth_service()
        self.cookie_service = get_cookie_service()
        self.log = get_logger_service(__name__)

    @logout_swagger
    def post(self, request: Request) -> Response:
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data.get("refresh_token")

        response = build_success_response(
            data=None,
            status_code=status.HTTP_200_OK,
        )

        self.cookie_service.delete_cookie(response)

        self.log.info("User logged out successfully.")
        return response
