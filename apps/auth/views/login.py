from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.container import get_auth_service, get_cookie_service, get_jwt_service
from apps.auth.dto import LoginEmailRequestDTO, LoginResponseDTO
from apps.auth.serializers.login import LoginSerializer
from apps.auth.services.auth import AuthService
from apps.auth.services.cookie import CookieService
from apps.auth.services.jwt import JWTService
from apps.auth.swagger.login import login_request_example, login_response_example
from apps.core.logger import LoggerType, factory_logger


class LoginViaEmailView(views.APIView):
    auth_service: AuthService
    log: LoggerType

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)

        self.log = factory_logger(__name__)
        self.auth_service = get_auth_service()

    @swagger_auto_schema(
        request_body=login_request_example,
        responses={200: login_response_example},
        tags=["Authentication"],
    )
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto: LoginEmailRequestDTO = serializer.validated_data
        login_response: LoginResponseDTO = self.auth_service.login_email(dto)

        response = Response(login_response, status=200)

        response = self.auth_service.cookie_svc.set_cookie(
            response, login_response["refresh_token"]
        )

        self.log.info("Login successful user_id=%s", login_response["user"]["id"])

        return response


class LoginViaPhoneView(views.APIView):
    cookie_service: CookieService
    jwt_service: JWTService

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)

        self.cookie_service = get_cookie_service()
        self.jwt_service = get_jwt_service()

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: "access_token: str"},
        tags=["Authentication"],
    )
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        access_token = self.jwt_service.create_access_token(user)
        refresh_token = self.jwt_service.create_refresh_token(user)

        response = Response({"access_token": access_token}, status=status.HTTP_200_OK)

        response = self.cookie_service.set_cookie(response, refresh_token)
        return response
