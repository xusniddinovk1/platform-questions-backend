from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.questions.repositories.question import QuestionRepository
from apps.questions.serializers.question import QuestionSerializer
from apps.questions.services.question import QuestionService

question_service = QuestionService(repo=QuestionRepository())


class QuestionListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = question_service.list_questions()
        return Response(QuestionSerializer(qs, many=True).data, status=status.HTTP_200_OK)


class QuestionDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk: int):
        question = question_service.get_question(pk)
        return Response(QuestionSerializer(question).data, status=status.HTTP_200_OK)
