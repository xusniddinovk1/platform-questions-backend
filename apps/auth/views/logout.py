from drf_yasg.utils import swagger_auto_schema
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.container import get_cookie_service
from apps.auth.services.cookie_service import CookieService


class LogoutView(views.APIView):
    cookie_service: CookieService

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)

        self.cookie_service = get_cookie_service()

    @swagger_auto_schema(response={200: "message: str"}, tags=["Authentication"])
    def post(self, request: Request) -> Response:
        response = Response({"message": "Logged out"})
        response.delete_cookie(self.cookie_service.cookie_name)
        return response
