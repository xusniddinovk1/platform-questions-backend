from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.questions.repositories.question import QuestionRepository
from apps.questions.serializers.question import QuestionSerializer
from apps.questions.services.question import QuestionService

question_service = QuestionService(repo=QuestionRepository())


class QuestionListAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request: Request) -> Response:
        qs = question_service.list_questions()
        data = QuestionSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class QuestionDetailAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request: Request, pk: int) -> Response:
        question = question_service.get_question(pk)
        return Response(
            QuestionSerializer(question).data,
            status=status.HTTP_200_OK,
        )
