from rest_framework import views, status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.container import get_auth_service, get_cookie_service
from apps.auth.dto import LoginEmailRequestDTO, LoginResponseDTO
from apps.auth.serializers.login import LoginSerializer
from apps.auth.services.auth import AuthService
from apps.auth.services.cookie import CookieService
from apps.auth.swagger.login import login_schema_swagger
from apps.core.responses import build_success_response
from apps.core.logger import LoggerType, get_logger_service


class LoginViaEmailView(views.APIView):
    auth_service: AuthService
    cookie_service: CookieService
    log: LoggerType

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)

        self.log = get_logger_service(__name__)
        self.auth_service = get_auth_service()
        self.cookie_service = get_cookie_service()

    @login_schema_swagger
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto: LoginEmailRequestDTO = serializer.validated_data
        login_response: LoginResponseDTO = self.auth_service.login_email(dto)

        response = build_success_response(
            data=login_response,
            status_code=status.HTTP_200_OK,
        )

        response = self.cookie_service.set_cookie(
            response, login_response["refresh_token"]
        )

        self.log.info("Login successful user_id=%s", login_response["user"]["id"])

        return response
