from drf_yasg.utils import swagger_auto_schema
from rest_framework import views
from rest_framework.request import Request


class OAuthGoogleView(views.APIView):
    @swagger_auto_schema(
        operation_description="Login via Google OAuth", tags=["OAuth", "Authentication"]
    )
    def post(self, request: Request) -> None:
        pass
