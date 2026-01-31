from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.auth.serializers.profile import (
    ProfileRequestSerializer,
    ProfileResponeSerializer,
)

profile_swagger = swagger_auto_schema(
    operation_summary="Get user profile",
    operation_description=(
        "Возвращает профиль текущего пользователя.\n\n"
        "🔐 **Web**: refresh token берётся из HttpOnly cookie.\n"
        "📱 **Mobile**: refresh token передаётся в body запроса.\n\n"
        "Если refresh token отсутствует или невалиден — возвращается 401."
    ),
    request_body=ProfileRequestSerializer,
    responses={
        200: openapi.Response(
            description="Профиль пользователя",
            schema=ProfileResponeSerializer,
        ),
        401: openapi.Response(
            description="Refresh token отсутствует или невалиден",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Unauthorized",
                    )
                },
            ),
        ),
    },
    tags=["Authentication"],
)
