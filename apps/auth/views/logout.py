from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.container import get_auth_service, get_cookie_service
from apps.auth.serializers.logout import LogoutSerializer
from apps.auth.services.auth import AuthService
from apps.auth.services.cookie import CookieService
from apps.auth.swagger.logout import logout_swagger
from apps.core.logger import LoggerType, factory_logger


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
        self.log = factory_logger(__name__)

    @logout_swagger
    def post(self, request: Request) -> Response:
        response = Response(status=204)

        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data.get("refresh_token")

        self.cookie_service.delete_cookie(response)

        self.log.info("User logged out successfully.")
        return response
