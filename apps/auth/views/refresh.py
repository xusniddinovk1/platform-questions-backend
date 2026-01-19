from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.container import get_cookie_service, get_jwt_service
from apps.auth.services.cookie_service import CookieService
from apps.auth.services.jwt_service import JWTService


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
        refresh_token = request.COOKIES.get(self.cookie_service.cookie_name)
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
