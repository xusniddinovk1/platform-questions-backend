from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.container import get_auth_service, get_cookie_service
from apps.auth.dto.token import RefreshTokenRequestDTO
from apps.auth.exceptions.invalid_token import InvalidToken
from apps.auth.services.auth import AuthService
from apps.auth.services.cookie import CookieService
from apps.auth.swagger.refresh import refresh_token_swagger
from apps.core.logger import LoggerType, factory_logger


class RefreshView(views.APIView):
    auth_service: AuthService
    cookie_service: CookieService
    log: LoggerType

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)

        self.auth_service = get_auth_service()
        self.cookie_service = get_cookie_service()
        self.log = factory_logger(__name__)

    @refresh_token_swagger
    def post(self, request: Request) -> Response:
        refresh_token = request.COOKIES.get(self.cookie_service.cookie_name)

        if not refresh_token:
            self.log.error("No refresh token")
            return Response(
                {"error": "No refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        dto: RefreshTokenRequestDTO = {
            "refresh_token": refresh_token,
        }

        try:
            result = self.auth_service.refresh_token(dto)
        except InvalidToken:
            self.log.error("Invalid token")
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response({"access_token": result["access_token"]})
        self.cookie_service.set_cookie(response, result["refresh_token"])

        self.log.info("Token refreshed")
        return response
