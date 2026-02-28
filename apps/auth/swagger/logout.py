from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.core.swagger.common import envelope_schema

logout_request_example = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "refresh_token": openapi.Schema(
            type=openapi.TYPE_STRING,
            description=(
                "Refresh token пользователя.\n\n"
                "🌐 WEB: не передаётся в body, хранится в HttpOnly cookie.\n"
                "📱 MOBILE: передаётся в body запроса."
            ),
        ),
    },
    required=[],
    example={"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
)

refresh_token_cookie_param = openapi.Parameter(
    name="refresh_token",
    in_=openapi.IN_HEADER,
    description=(
        "HttpOnly refresh token.\n\n"
        "🌐 WEB: автоматически передаётся браузером.\n"
        "⚠️ Swagger UI не может отправить HttpOnly cookie."
    ),
    type=openapi.TYPE_STRING,
    required=False,
)


logout_swagger = swagger_auto_schema(
    operation_summary="Logout",
    operation_description=(
        "Выход пользователя из системы.\n\n"
        "🌐 **WEB**:\n"
        "- Refresh token хранится в HttpOnly cookie\n"
        "- Cookie удаляется сервером\n\n"
        "📱 **MOBILE**:\n"
        "- Refresh token передаётся в body\n"
        "- Клиент удаляет token локально\n\n"
        "✅ Возвращает `200 OK` с общей схемой ответа"
    ),
    request_body=logout_request_example,
    manual_parameters=[refresh_token_cookie_param],
    responses={
        200: openapi.Response(
            description="User logged out successfully",
            schema=envelope_schema(
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="В поле data ничего нет при успешном логауте",
                )
            ),
            examples={
                "application/json": {
                    "data": None,
                    "meta": {},
                    "errors": None,
                }
            },
        ),
    },
    tags=["Authentication"],
)
