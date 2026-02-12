from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from apps.questions.repositories.answer import AnswerRepository
from apps.questions.repositories.question import QuestionRepository
from apps.questions.serializers.answer import AnswerSerializer
from apps.questions.services.answer import (
    AnswerService,
    CreateAnswerCommand,
    AnswerAlreadyExists,
    AnswerTypeNotAllowed,
)

answer_service = AnswerService(
    question_repo=QuestionRepository(),
    answer_repo=AnswerRepository(),
)


class AnswerListByQuestionAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, question_id: int):
        answers = answer_service.list_by_question(question_id)
        return Response(AnswerSerializer(answers, many=True).data, status=status.HTTP_200_OK)


class AnswerCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cmd = CreateAnswerCommand(
            question_id=int(request.data.get("question")),
            user_id=int(request.user.id),
            content=request.data.get("content") or {},
        )

        try:
            answer = answer_service.create_answer(cmd)
        except AnswerAlreadyExists:
            raise ValidationError("Siz bu savolga allaqachon javob bergansiz.")
        except AnswerTypeNotAllowed as e:
            raise ValidationError(
                {"content": f"Ruxsat etilgan turlar: {e.allowed}. Siz yubordingiz: {e.sent}"}
            )
        except serializers.ValidationError as e:
            raise ValidationError(e.detail)

        return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED)
