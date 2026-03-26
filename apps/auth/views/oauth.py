from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.container import (
    get_auth_service,
    get_cookie_service,
    get_google_oauth_service,
)
from apps.auth.dto.google_oauth import (
    GoogleAuthURLResponseDTO,
    GoogleCallbackResponseDTO,
)
from apps.auth.exceptions.google_oauth import GoogleEmailNotVerified, GoogleOAuthError
from apps.auth.serializers.google_oauth import GoogleCallbackSerializer
from apps.auth.services.auth import AuthService
from apps.auth.services.cookie import CookieService
from apps.auth.services.google_oauth import GoogleOAuthService
from apps.auth.swagger.google_oauth import (
    google_auth_url_swagger,
    google_callback_swagger,
)
from apps.core.logger import LoggerType, get_logger_service
from apps.core.responses import build_error_response, build_success_response


class GoogleAuthURLView(views.APIView):
    """Returns the Google OAuth 2.0 authorization URL."""

    google_svc: GoogleOAuthService
    log: LoggerType

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)
        self.log = get_logger_service(__name__)
        self.google_svc = get_google_oauth_service()

    @google_auth_url_swagger
    def get(self, request: Request) -> Response:
        state = self.google_svc.generate_state_token()
        url = self.google_svc.build_authorization_url(state)

        data = GoogleAuthURLResponseDTO(authorization_url=url)
        return build_success_response(data=data)


class GoogleCallbackView(views.APIView):
    """Exchanges a Google authorization code for JWT tokens."""

    google_svc: GoogleOAuthService
    auth_svc: AuthService
    cookie_svc: CookieService
    log: LoggerType

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)
        self.log = get_logger_service(__name__)
        self.google_svc = get_google_oauth_service()
        self.auth_svc = get_auth_service()
        self.cookie_svc = get_cookie_service()

    @google_callback_swagger
    def post(self, request: Request) -> Response:
        serializer = GoogleCallbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if not self.google_svc.verify_state_token(data["state"]):
            self.log.warning("Google OAuth: invalid or expired state token")
            return build_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                code="INVALID_STATE",
                title="Invalid state token",
                detail="""The state parameter
                is invalid or expired. Please retry the flow.""",
            )

        try:
            google_user = self.google_svc.authenticate(data["code"])
        except ValueError as exc:
            self.log.error("Google OAuth token exchange failed: %s", exc)
            return build_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                code="GOOGLE_AUTH_FAILED",
                title="Google authentication failed",
                detail="Could not verify the authorization code with Google.",
            )

        try:
            result: GoogleCallbackResponseDTO = self.auth_svc.login_or_register_google(
                google_user
            )
        except GoogleEmailNotVerified:
            self.log.warning(
                "Google OAuth: email %s is not verified", google_user["email"]
            )
            return build_error_response(
                status_code=status.HTTP_403_FORBIDDEN,
                code="EMAIL_NOT_VERIFIED",
                title="Email not verified",
                detail="Your Google account email is not verified.",
            )
        except GoogleOAuthError as exc:
            self.log.error("Google OAuth error: %s", exc)
            return build_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                code="GOOGLE_AUTH_ERROR",
                title="Google authentication error",
                detail="An unexpected error occurred during Google authentication.",
            )

        response = build_success_response(data=result, status_code=status.HTTP_200_OK)
        response = self.cookie_svc.set_cookie(response, result["refresh_token"])

        action = "registered" if result["is_new_user"] else "logged in"
        self.log.info(
            "Google OAuth: user %s %s (id=%s)",
            result["user"]["email"],
            action,
            result["user"]["id"],
        )

        return response
