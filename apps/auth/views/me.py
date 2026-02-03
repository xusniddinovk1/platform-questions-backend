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


class MeView(APIView):
    me_service: MeService
    log: LoggerType

    def __init__(self) -> None:
        super().__init__()
        self.me_service = get_me_service()
        self.log = get_logger_service(__name__)

    @me_swagger
    def get(self, request: Request) -> Response:
        accest_token = request.headers.get("Authorization", "").split("Bearer ")[-1]

        if not accest_token:
            self.log.warning("Access token is missing in the request headers")
            return Response({"detail": "Access token is required"}, status=401)

        try:
            user: User | None = self.me_service.get_me(accest_token)
        except InvalidToken:
            self.log.warning("Invalid access token")
            return Response({"detail": "Invalid access token"}, status=401)
        except TokenExpired:
            self.log.warning("Access token has expired")
            return Response({"detail": "Access token has expired"}, status=401)

        if not user:
            self.log.warning("User not found for the provided access token")
            return Response({"detail": "User not found"}, status=404)

        dto: MeResponseDTO = MeResponseDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            last_name=user.last_name,
            first_name=user.first_name,
            is_active=user.is_active,
            role=user.role,
        )

        return Response(dto, status=200)
