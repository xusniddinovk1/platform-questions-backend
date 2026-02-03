from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

email_confirm_swagger = swagger_auto_schema(
    operation_summary="Подтверждение email пользователя",
    operation_description=(
        "Подтверждает email пользователя по ссылке из письма.\n\n"
        "🔗 **Ссылка**: `GET /v1/auth/confirm/<uidb64>/<token>/`\n\n"
        "📌 **WEB**:\n"
        "- После успешного подтверждения происходит redirect на фронтенд:\n"
        "  `{FRONTEND_URL}/email-confirm?status=success`\n"
        "- Если токен недействителен или пользователь не найден:\n"
        "  `{FRONTEND_URL}/email-confirm?status=invalid`\n\n"
        "📱 **MOBILE / API clients**:\n"
        "- Можно получать статус подтверждения через JSON (если изменить логику)\n\n"
        "✅ **Поведение**:\n"
        "- Пользователь активируется (`is_active=True`) при успешной проверке токена\n"
        "- Недействительные или просроченные токены отклоняются"
    ),
    manual_parameters=[
        openapi.Parameter(
            name="uidb64",
            in_=openapi.IN_PATH,
            description="Закодированный ID пользователя (base64).",
            type=openapi.TYPE_STRING,
            required=True,
            example="Mg",
        ),
        openapi.Parameter(
            name="token",
            in_=openapi.IN_PATH,
            description="Токен подтверждения, сгенерированный при регистрации.",
            type=openapi.TYPE_STRING,
            required=True,
            example="d3ds6h-9bdfad662f20ce948ddb1664f82ecce7",
        ),
    ],
    responses={
        302: openapi.Response(
            description="Redirect на frontend c параметром"
            "?status=success или ?status=invalid"
        ),
        400: openapi.Response(description="Некорректный запрос"),
        404: openapi.Response(description="Пользователь не найден или токен неверен"),
    },
    tags=["Authentication"],
)
