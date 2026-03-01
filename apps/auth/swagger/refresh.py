from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.core.swagger.common import envelope_schema

refresh_token_request_example = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "refresh_token": openapi.Schema(
            type=openapi.TYPE_STRING,
            description=(
                "Refresh token пользователя.\n\n"
                "⚠️ Для WEB-приложений передаётся автоматически "
                "через HttpOnly cookie и **не передаётся в body**.\n"
                "📱 Для mobile-приложений может передаваться явно."
            ),
        )
    },
    required=["refresh_token"],
    example={"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
)

refresh_token_data_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access_token": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Новый access token пользователя",
        ),
        "refresh_token": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Новый refresh token пользователя",
        ),
    },
    required=["access_token", "refresh_token"],
)

refresh_token_success_response_schema = envelope_schema(refresh_token_data_schema)


auth_error_response_example = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "error": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Описание ошибки аутентификации",
        ),
    },
    required=["error"],
    example={"error": "Invalid token"},
)


refresh_token_swagger = swagger_auto_schema(
    operation_summary="Refresh access token",
    operation_description=(
        "Обновляет access token пользователя по refresh token.\n\n"
        "🔐 Refresh token хранится в HttpOnly cookie (WEB).\n"
        "📱 Для mobile-клиентов refresh token может передаваться в body."
    ),
    request_body=refresh_token_request_example,
    responses={
        200: openapi.Response(
            description="Access token успешно обновлён",
            schema=refresh_token_success_response_schema,
            examples={
                "application/json": {
                    "data": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    },
                    "meta": {
                        "pagination": {
                            "page": 1,
                            "limit": 10,
                            "total": 1,
                            "totalPages": 1,
                        }
                    },
                    "errors": None,
                }
            },
        ),
        401: openapi.Response(
            description="Refresh token отсутствует или невалиден",
            schema=envelope_schema(auth_error_response_example),
            examples={
                "application/json": {
                    "data": None,
                    "meta": {},
                    "errors": [
                        {
                            "status": 401,
                            "code": "INVALID_REFRESH_TOKEN",
                            "title": "Invalid refresh token",
                            "detail": "Refresh token is invalid",
                        }
                    ],
                }
            },
        ),
    },
    tags=["Authentication"],
)
