from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.core.swagger.common import envelope_schema

# ── GET /auth/google/url/ ─────────────────────────────────────────

google_url_data_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "authorization_url": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Full Google OAuth authorization URL (redirect the user here)",
        ),
    },
)

google_auth_url_swagger = swagger_auto_schema(
    operation_description=(
        "Returns the Google OAuth 2.0 authorization URL.\n\n"
        "The frontend should redirect the user to this URL. "
        "After the user consents, Google redirects to "
        "`GOOGLE_REDIRECT_URI` with `code` and `state` query parameters."
    ),
    responses={
        200: openapi.Response(
            description="Authorization URL generated",
            schema=envelope_schema(google_url_data_schema),
            examples={
                "application/json": {
                    "data": {
                        "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?..."
                    },
                    "meta": {},
                    "errors": None,
                }
            },
        ),
    },
    tags=["Authentication"],
)

# ── POST /auth/google/callback/ ──────────────────────────────────

google_callback_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "code": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Authorization code from Google redirect",
        ),
        "state": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="State token returned by Google (CSRF protection)",
        ),
    },
    required=["code", "state"],
    example={
        "code": "4/0AX4XfWh...",
        "state": "eyJhbGciOiJIUzI1NiJ9...",
    },
)

google_callback_data_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access_token": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="JWT access token",
        ),
        "refresh_token": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="JWT refresh token",
        ),
        "user": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        "is_new_user": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description="True when the user was just created",
        ),
    },
)

google_callback_swagger = swagger_auto_schema(
    operation_description=(
        "Exchange a Google authorization code for JWT tokens.\n\n"
        "1. The frontend obtains `code` and `state` from the Google redirect.\n"
        "2. Send them here; the backend verifies the state, exchanges the code "
        "with Google, validates the ID-token, and creates or logs in the user.\n"
        "3. A refresh-token cookie is also set (HttpOnly)."
    ),
    request_body=google_callback_request_schema,
    responses={
        200: openapi.Response(
            description="User authenticated via Google",
            schema=envelope_schema(google_callback_data_schema),
            examples={
                "application/json": {
                    "data": {
                        "access_token": "eyJhbGciOiJIUzI1...",
                        "refresh_token": "dGhpcy1pcy1yZWZyZXNoLXRva2Vu",
                        "user": {
                            "id": 1,
                            "email": "user@gmail.com",
                            "username": "user",
                            "first_name": "Ivan",
                            "last_name": "Ivanov",
                        },
                        "is_new_user": True,
                    },
                    "meta": {},
                    "errors": None,
                }
            },
        ),
        400: openapi.Response(description="Invalid state or code"),
        403: openapi.Response(description="Google email not verified"),
    },
    tags=["Authentication"],
)
