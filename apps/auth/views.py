from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.container import get_cookie_service, get_jwt_service

from .serializers import LoginSerializer, RegisterSerializer
from .services.cookie_service import CookieService
from .services.jwt_service import JWTService


class RegisterView(views.APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: "Пользователь зарегистрирован"},
        tags=["Authentication"],
    )
    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Пользователь зарегистрирован"}, status=status.HTTP_201_CREATED
        )


class LoginView(views.APIView):
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


class RefreshView(views.APIView):
    jwt_service: JWTService
    cookie_service: CookieService

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)

        self.jwt_service = get_jwt_service()
        self.cookie_service = get_cookie_service()

    @swagger_auto_schema(
        responses={200: "access_token: str", 401: "Invalid token"},
        tags=["Authentication"],
    )
    def post(self, request: Request) -> Response:
        refresh_token = request.COOKIES.get(self.cookie_service.COOKIE_NAME)
        if not refresh_token:
            return Response(
                {"error": "No refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        user = self.jwt_service.decode_token(refresh_token)
        if not user:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        if not user:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = self.jwt_service.create_access_token(user)
        return Response({"access_token": access_token})


class LogoutView(views.APIView):
    cookie_service: CookieService

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)

        self.cookie_service = get_cookie_service()

    @swagger_auto_schema(response={200: "message: str"}, tags=["Authentication"])
    def post(self, request: Request) -> Response:
        response = Response({"message": "Logged out"})
        response.delete_cookie(self.cookie_service.COOKIE_NAME)
        return response
