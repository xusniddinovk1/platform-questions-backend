from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """
    Простая проверка здоровья сервиса.
    """

    def get(self, request: Request) -> Response:
        # request.status_code в DRF всегда 200 на момент запроса,
        # если нужен статус ответа — см. response
        print(request.method)  # пример логирования
        return Response({"ok": "True"}, status=status.HTTP_200_OK)
