from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.container import get_auth_service
from apps.auth.dto import RegisterRequestDTO, RegisterResponseDTO
from apps.auth.serializers.register import RegisterEmailSerializer
from apps.auth.services.auth import AuthService
from apps.auth.swagger.register import register_request_example, register_response_example
from apps.core.logger import LoggerType, factory_logger


class RegisterEmailView(views.APIView):
    auth_service: AuthService
    log: LoggerType

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)
        self.log = factory_logger(__name__)
        self.auth_service = get_auth_service()

    @swagger_auto_schema(
        request_body=register_request_example,
        responses={201: register_response_example},
        tags=["Authentication"],
    )
    def post(self, request: Request) -> Response:
        """
        Регистрация пользователя по email.
        Входные данные: RegisterRequestDTO
        Выходные данные: RegisterResponseDTO c access и refresh токенами.
        """
        serializer = RegisterEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data: RegisterRequestDTO = serializer.validated_data

        register_response: RegisterResponseDTO = self.auth_service.register_email(
            dto=user_data
        )

        self.log.info(f"User {user_data['email']} registered")

        return Response(
            register_response,
            status=status.HTTP_201_CREATED,
        )
