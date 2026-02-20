from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.questions.repositories.answer import AnswerRepository
from apps.questions.repositories.question import QuestionRepository
from apps.questions.serializers.answer import AnswerSerializer, AnswerCreateSerializer
from apps.questions.services.answer import (
    AnswerAlreadyExists,
    AnswerService,
    AnswerTypeNotAllowed,
    CreateAnswerCommand,
)

answer_service = AnswerService(
    question_repo=QuestionRepository(),
    answer_repo=AnswerRepository(),
)

class AnswerCreateAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request: Request) -> Response:
        serializer = AnswerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = request.user.id
        if user_id is None:
            raise ValidationError({"user": "User topilmadi."})

        cmd = CreateAnswerCommand(
            question_id=serializer.validated_data["question_id"],
            user_id=user_id,
            content_type=serializer.validated_data["content"]["content_type"],
            payload=serializer.validated_data["content"],
        )

        try:
            answer = answer_service.create_answer(cmd)
        except AnswerAlreadyExists:
            raise ValidationError("Siz bu savolga allaqachon javob bergansiz.")
        except AnswerTypeNotAllowed as e:
            msg = (
                f"Ruxsat etilgan turlar: {e.allowed}. "
                f"Siz yubordingiz: {e.sent}"
            )
            raise ValidationError({"content": msg})

        return Response(
            AnswerSerializer(answer).data,
            status=status.HTTP_201_CREATED,
        )