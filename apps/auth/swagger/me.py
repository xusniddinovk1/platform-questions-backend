from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.core.swagger.common import envelope_schema

me_data_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            example=1,
            description="ID пользователя",
        ),
        "username": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="john_doe",
            description="Username пользователя",
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="john@example.com",
            description="Email пользователя",
        ),
        "first_name": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="John Doe",
            description="Полное имя пользователя",
        ),
        "last_name": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="Doe",
            description="Фамилия пользователя",
        ),
        "is_active": openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            example=True,
            description="Активен ли пользователь",
        ),
        "role": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="user",
            description="Роль пользователя",
        ),
    },
)

me_swagger = swagger_auto_schema(
    operation_summary="Получение текущего пользователя",
    operation_description=(
        "Возвращает информацию o текущем авторизованном пользователе.\n\n"
        "🔐 **Авторизация**:\n"
        "- Access token передаётся через заголовок `Authorization: Bearer <token>`\n\n"
        "🌐 **WEB**:\n"
        "- Access token берётся из `Authorization` header\n\n"
        "📱 **Mobile**:\n"
        "- Access token также передаётся в `Authorization` header"
    ),
    manual_parameters=[
        openapi.Parameter(
            name="Authorization",
            in_=openapi.IN_HEADER,
            description="Access token в формате: `Bearer <access_token>`",
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: openapi.Response(
            description="Данные текущего пользователя",
            schema=envelope_schema(me_data_schema),
        ),
        401: openapi.Response(
            description="Access token не передан или невалиден",
            schema=envelope_schema(
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Access token is required",
                        ),
                    },
                )
            ),
        ),
        404: openapi.Response(
            description="Пользователь не найден",
            schema=envelope_schema(
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="User not found",
                        ),
                    },
                )
            ),
        ),
    },
    tags=["Authentication"],
)
