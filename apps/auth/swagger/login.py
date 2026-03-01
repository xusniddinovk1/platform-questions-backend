from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.core.swagger.common import envelope_schema

login_request_example = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(
            type=openapi.TYPE_STRING, description="Email пользователя"
        ),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description="Пароль"),
    },
    required=["email", "password"],
    example={"email": "user@example.com", "password": "strongpassword123"},
)


login_data_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access_token": openapi.Schema(
            type=openapi.TYPE_STRING, description="JWT access token"
        ),
        "refresh_token": openapi.Schema(
            type=openapi.TYPE_STRING, description="JWT refresh token"
        ),
        "user": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "username": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    },
)

login_success_response_schema = envelope_schema(login_data_schema)


login_schema_swagger = swagger_auto_schema(
    request_body=login_request_example,
    responses={
        200: openapi.Response(
            description="Успешный логин",
            schema=login_success_response_schema,
            examples={
                "application/json": {
                    "data": {
                        "access_token": "eyJhbGciOiJIUzI1...",
                        "refresh_token": "dGhpcy1pcy1yZWZyZXNoLXRva2Vu",
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "username": "user123",
                        },
                    },
                    "meta": {},
                    "errors": None,
                }
            },
        )
    },
    tags=["Authentication"],
)
