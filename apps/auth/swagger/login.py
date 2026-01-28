from drf_yasg import openapi

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


login_response_example = openapi.Schema(
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
    example={
        "access_token": "eyJhbGciOiJIUzI1...",
        "refresh_token": "dGhpcy1pcy1yZWZyZXNoLXRva2Vu",
        "user": {"id": 1, "email": "user@example.com", "username": "user123"},
    },
)
