from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.container import get_cookie_service, get_jwt_service
from apps.auth.serializers.login import LoginSerializer
from apps.auth.services.cookie_service import CookieService
from apps.auth.services.jwt_service import JWTService


class LoginViaEmailView(views.APIView):
    cookie_service: CookieService
    jwt_service: JWTService

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)

        self.cookie_service = get_cookie_service()
        self.jwt_service = get_jwt_service()

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: "access_token: str"},
        tags=["Authentication"],
    )
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        access_token = self.jwt_service.create_access_token(user)
        refresh_token = self.jwt_service.create_refresh_token(user)

        response = Response({"access_token": access_token}, status=status.HTTP_200_OK)

        response = self.cookie_service.set_cookie(response, refresh_token)
        return response


class LoginViaPhoneView(views.APIView):
    cookie_service: CookieService
    jwt_service: JWTService

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)

        self.cookie_service = get_cookie_service()
        self.jwt_service = get_jwt_service()

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: "access_token: str"},
        tags=["Authentication"],
    )
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        access_token = self.jwt_service.create_access_token(user)
        refresh_token = self.jwt_service.create_refresh_token(user)

        response = Response({"access_token": access_token}, status=status.HTTP_200_OK)

        response = self.cookie_service.set_cookie(response, refresh_token)
        return response
