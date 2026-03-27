from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.container import get_me_service
from apps.auth.dto.me import MeResponseDTO, MeUpdateRequestDTO
from apps.auth.exceptions.invalid_token import InvalidToken
from apps.auth.exceptions.token_expired import TokenExpired
from apps.auth.serializers.me import MeUpdateSerializer
from apps.auth.services.me import MeService
from apps.auth.swagger.me import me_swagger
from apps.auth.swagger.me_update import me_update_swagger
from apps.core.logger import LoggerType, get_logger_service
from apps.core.responses import build_error_response, build_success_response
from apps.user.exceptions.user_not_found import UserNotFoundException
from apps.user.models import User

from apps.auth.permissions import IsAuthenticatedUser


class MeView(APIView):
    me_service: MeService
    log: LoggerType

    permission_classes = (IsAuthenticatedUser,)

    def __init__(self) -> None:
        super().__init__()
        self.me_service = get_me_service()
        self.log = get_logger_service(__name__)

    @me_swagger
    def get(self, request: Request) -> Response:
        accest_token = request.headers.get("Authorization", "")
        accest_token = accest_token.replace("Bearer ", "", 1).strip()

        if not accest_token:
            self.log.warning("Access token is missing in the request headers")
            return build_error_response(
                status_code=401,
                code="ACCESS_TOKEN_REQUIRED",
                title="Access token is required",
                detail="Access token must be provided in the Authorization header",
            )

        try:
            user: User | None = self.me_service.get_me(accest_token)
        except InvalidToken:
            self.log.warning("Invalid access token")
            return build_error_response(
                status_code=401,
                code="INVALID_ACCESS_TOKEN",
                title="Invalid access token",
                detail="Access token is invalid",
            )
        except TokenExpired:
            self.log.warning("Access token has expired")
            return build_error_response(
                status_code=401,
                code="ACCESS_TOKEN_EXPIRED",
                title="Access token has expired",
                detail="Access token has expired",
            )

        if not user:
            self.log.warning("User not found for the provided access token")
            return build_error_response(
                status_code=404,
                code="USER_NOT_FOUND",
                title="User not found",
                detail="User not found for the provided access token",
            )

        dto: MeResponseDTO = MeResponseDTO(
            id=user.pk,
            email=user.email,
            username=user.username,
            last_name=user.last_name,
            first_name=user.first_name,
            is_active=user.is_active,
            role=user.role,
            university=user.university,
            birthday=user.birthday,
        )

        return build_success_response(dto)

    @me_update_swagger
    def patch(self, request: Request) -> Response:
        """
        Частичное обновление данных текущего пользователя.
        """
        access_token = request.headers.get("Authorization", "")
        access_token = access_token.replace("Bearer ", "", 1).strip()

        if not access_token:
            self.log.warning("Access token is missing in the request headers")
            return build_error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="ACCESS_TOKEN_REQUIRED",
                title="Access token is required",
                detail="Access token must be provided in the Authorization header",
            )

        serializer = MeUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            self.log.warning(
                "Validation error on updating current user: %s", serializer.errors
            )
            return build_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                code="VALIDATION_ERROR",
                title="Validation error",
                detail=str(serializer.errors),
            )

        dto: MeUpdateRequestDTO = serializer.validated_data

        try:
            user = self.me_service.update_me(access_token, dto)
        except InvalidToken:
            self.log.warning("Invalid access token on update")
            return build_error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="INVALID_ACCESS_TOKEN",
                title="Invalid access token",
                detail="Access token is invalid",
            )
        except TokenExpired:
            self.log.warning("Access token has expired on update")
            return build_error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="ACCESS_TOKEN_EXPIRED",
                title="Access token has expired",
                detail="Access token has expired",
            )
        except UserNotFoundException:
            self.log.warning("User not found for the provided access token on update")
            return build_error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                code="USER_NOT_FOUND",
                title="User not found",
                detail="User not found for the provided access token",
            )

        response_dto: MeResponseDTO = MeResponseDTO(
            id=user.pk,
            email=user.email,
            username=user.username,
            last_name=user.last_name,
            first_name=user.first_name,
            is_active=user.is_active,
            role=user.role,
            university=user.university,
            birthday=user.birthday,
        )

        return build_success_response(response_dto)
