from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.auth.swagger.me import me_data_schema
from apps.core.swagger.common import envelope_schema

me_update_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Новый username пользователя",
            example="new_username",
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Новый email пользователя",
            example="new_email@example.com",
        ),
        "first_name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Новое имя пользователя",
            example="Иван",
        ),
        "last_name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Новая фамилия пользователя",
            example="Иванов",
        ),
        "university": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Новый университет пользователя",
            example="MIT",
        ),
        "birthday": openapi.Schema(
            type=openapi.TYPE_STRING,
            format="date",
            description="Новая дата рождения пользователя",
            example="1990-01-01",
        ),
    },
)


me_update_swagger = swagger_auto_schema(
    operation_summary="Частичное обновление текущего пользователя",
    operation_description=(
        "Позволяет частично обновить данные текущего авторизованного пользователя.\n\n"
        "🔐 **Авторизация**:\n"
        "- Access token передаётся через заголовок `Authorization: Bearer <token>`\n\n"
        "Тело запроса может содержать один или несколько полей для обновления."
    ),
    request_body=me_update_request_schema,
    responses={
        200: openapi.Response(
            description="Данные пользователя успешно обновлены",
            schema=envelope_schema(me_data_schema),
        ),
        400: openapi.Response(
            description="Ошибка валидации входных данных",
            schema=envelope_schema(
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="{'email': ['Enter a valid email address.']}",
                        ),
                    },
                )
            ),
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
