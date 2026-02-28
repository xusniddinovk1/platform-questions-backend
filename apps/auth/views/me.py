from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.container import get_me_service
from apps.auth.dto.me import MeResponseDTO
from apps.auth.exceptions.invalid_token import InvalidToken
from apps.auth.exceptions.token_expired import TokenExpired
from apps.auth.services.me import MeService
from apps.auth.swagger.me import me_swagger
from apps.core.logger import LoggerType, get_logger_service
from apps.user.models import User
from apps.core.responses import build_error_response, build_success_response


class MeView(APIView):
    me_service: MeService
    log: LoggerType

    # permission_classes = (IsAuthenticated,)

    def __init__(self) -> None:
        super().__init__()
        self.me_service = get_me_service()
        self.log = get_logger_service(__name__)

    @me_swagger
    def get(self, request: Request) -> Response:
        accest_token = request.headers.get("Authorization", "").split("Bearer ")[-1]

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
        )

        return build_success_response(dto)
