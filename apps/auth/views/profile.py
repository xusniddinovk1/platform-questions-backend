from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.auth.container import get_cookie_service, get_profile_service
from apps.auth.permissions.role_permissions import IsUser
from apps.auth.serializers.profile import (
    ProfileRequestSerializer,
    ProfileResponeSerializer,
)
from apps.auth.services.cookie import CookieService
from apps.auth.services.profile import ProfileService
from apps.auth.swagger.profile import profile_swagger
from apps.core.responses import build_error_response, build_success_response
from apps.core.logger import LoggerType, get_logger_service


class ProfileView(APIView):
    log: LoggerType
    profile_service: ProfileService
    cookie_service: CookieService

    permission_classes = (IsAuthenticated, IsUser)

    def __init__(self) -> None:
        super().__init__()

        self.log = get_logger_service(__name__)
        self.profile_service = get_profile_service()
        self.cookie_service = get_cookie_service()

    @profile_swagger
    def post(self, request: Request) -> Response:
        serializer = ProfileRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Mobile
        refresh_token: str | None = serializer.validated_data.get("refresh_token")

        # Web
        if not refresh_token:
            refresh_token = self.cookie_service.get_cookie(request)

        if not refresh_token:
            self.log.warning("No refresh token found")
            return build_error_response(
                status_code=401,
                code="NO_REFRESH_TOKEN",
                title="No refresh token",
                detail="Refresh token is required",
            )

        profile_info = self.profile_service.get_user_profile(refresh_token)

        response_serializer = ProfileResponeSerializer(profile_info)
        return build_success_response(
            data=response_serializer.data,
        )
