from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.core.swagger.common import envelope_schema

register_request_example = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "first_name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Имя пользователя"
        ),
        "last_name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Фамилия пользователя"
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING, description="Email пользователя"
        ),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description="Пароль"),
    },
    required=["username", "first_name", "last_name", "email", "password"],
    example={
        "username": "user123",
        "first_name": "Иван",
        "last_name": "Иванов",
        "email": "user@example.com",
        "password": "strongpassword123",
    },
)


register_data_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access_token": openapi.Schema(
            type=openapi.TYPE_STRING, description="JWT access token"
        ),
        "refresh_token": openapi.Schema(
            type=openapi.TYPE_STRING, description="JWT refresh token"
        ),
    },
)

register_success_response_schema = envelope_schema(register_data_schema)


register_email_schema_swagger = swagger_auto_schema(
    request_body=register_request_example,
    responses={
        201: openapi.Response(
            description="Пользователь успешно зарегистрирован",
            schema=register_success_response_schema,
            examples={
                "application/json": {
                    "data": {
                        "access_token": "eyJhbGciOiJIUzI1...",
                        "refresh_token": "dGhpcy1pcy1yZWZyZXNoLXRva2Vu",
                    },
                    "meta": {},
                    "errors": None,
                }
            },
        )
    },
    tags=["Authentication"],
)
