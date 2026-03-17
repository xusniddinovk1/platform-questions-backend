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
            example="John",
            description="Имя пользователя",
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
            example="USER",
            description="Роль пользователя",
        ),
        "university": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="MIT",
            description="Университет пользователя",
        ),
        "birthday": openapi.Schema(
            type=openapi.TYPE_STRING,
            format="date",
            example="1990-01-01",
            description="Дата рождения пользователя",
        ),
    },
)

me_success_response_schema = envelope_schema(me_data_schema)

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
    responses={
        200: openapi.Response(
            description="Данные текущего пользователя",
            schema=me_success_response_schema,
            examples={
                "application/json": {
                    "data": {
                        "id": 1,
                        "username": "john_doe",
                        "email": "john@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "is_active": True,
                        "role": "USER",
                        "university": "MIT",
                        "birthday": "1990-01-01",
                    },
                    "meta": {},
                    "errors": None,
                }
            },
        ),
        401: openapi.Response(
            description="Access token не передан или невалиден",
            schema=envelope_schema(
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Access token is invalid",
                        ),
                    },
                )
            ),
            examples={
                "application/json": {
                    "data": None,
                    "meta": {},
                    "errors": [
                        {
                            "status": 401,
                            "code": "INVALID_ACCESS_TOKEN",
                            "title": "Invalid access token",
                            "detail": "Access token is invalid",
                        }
                    ],
                }
            },
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
            examples={
                "application/json": {
                    "data": None,
                    "meta": {},
                    "errors": [
                        {
                            "status": 404,
                            "code": "USER_NOT_FOUND",
                            "title": "User not found",
                            "detail": "User not found for the provided access token",
                        }
                    ],
                }
            },
        ),
    },
    tags=["Authentication"],
)
