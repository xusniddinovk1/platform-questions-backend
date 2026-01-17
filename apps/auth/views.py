from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import LoginSerializer, RegisterSerializer
from .services import create_access_token, create_refresh_token, decode_token

COOKIE_NAME = "refresh_token"


class RegisterView(views.APIView):
    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Пользователь зарегистрирован"}, status=status.HTTP_201_CREATED
        )


class LoginView(views.APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        response = Response({"access_token": access_token}, status=status.HTTP_200_OK)

        # Добавляем refresh token в httpOnly cookie
        response.set_cookie(
            key=COOKIE_NAME,
            value=refresh_token,
            httponly=True,
            samesite="Strict",
            max_age=7 * 24 * 60 * 60,
        )
        return response


class RefreshView(views.APIView):
    def post(self, request: Request) -> Response:
        refresh_token = request.COOKIES.get(COOKIE_NAME)
        if not refresh_token:
            return Response(
                {"error": "No refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        user = decode_token(refresh_token)
        if not user:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        if not user:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = create_access_token(user)
        return Response({"access_token": access_token})


class LogoutView(views.APIView):
    def post(self, request: Request) -> Response:
        response = Response({"message": "Logged out"})
        response.delete_cookie(COOKIE_NAME)
        return response
