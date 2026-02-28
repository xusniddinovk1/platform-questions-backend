from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.container import get_auth_service
from apps.auth.dto import RegisterResponseDTO
from apps.auth.dto.register import RegisterEmailRequestDTO
from apps.auth.exceptions.is_user_already_exists import IsUserAlreadyExists
from apps.auth.serializers.register import RegisterEmailSerializer
from apps.auth.services.auth import AuthService
from apps.auth.swagger.register import (
    register_email_schema_swagger,
)
from apps.core.responses import build_error_response, build_success_response
from apps.core.logger import LoggerType, get_logger_service


class RegisterEmailView(views.APIView):
    auth_service: AuthService
    log: LoggerType

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)
        self.log = get_logger_service(__name__)
        self.auth_service = get_auth_service()

    @register_email_schema_swagger
    def post(self, request: Request) -> Response:
        """
        Регистрация пользователя по email.
        Входные данные: RegisterRequestDTO
        Выходные данные: RegisterResponseDTO c access и refresh токенами.
        """
        serializer = RegisterEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data: RegisterEmailRequestDTO = serializer.validated_data

        try:
            register_response: RegisterResponseDTO = self.auth_service.register_email(
                dto=user_data
            )
        except IsUserAlreadyExists as e:
            self.log.error(f"User {user_data['email']} already exists")
            return build_error_response(
                status_code=status.HTTP_409_CONFLICT,
                code="USER_ALREADY_EXISTS",
                title="User already exists",
                detail=str(e),
            )
        except Exception as e:
            self.log.error(f"Error registering user {user_data['email']}: {e!s}")
            return build_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                code="INTERNAL_SERVER_ERROR",
                title="Internal server error",
                detail="Internal server error",
            )

        self.log.info(f"User {user_data['email']} registered")

        return build_success_response(
            data=register_response,
            status_code=status.HTTP_201_CREATED,
        )
