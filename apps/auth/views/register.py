from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.serializers.register import RegisterSerializer


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
