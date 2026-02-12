from rest_framework import permissions, serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.questions.repositories.answer import AnswerRepository
from apps.questions.repositories.question import QuestionRepository
from apps.questions.serializers.answer import AnswerSerializer
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
        question_raw = request.data.get("question")
        if question_raw is None:
            raise ValidationError({"question": "Majburiy."})

        user_id = request.user.id
        if user_id is None:
            raise ValidationError({"user": "User topilmadi."})

        cmd = CreateAnswerCommand(
            question_id=int(question_raw),
            user_id=int(user_id),
            content=request.data.get("content") or {},
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
        except serializers.ValidationError as e:
            raise ValidationError(e.detail) from e

        return Response(
            AnswerSerializer(answer).data,
            status=status.HTTP_201_CREATED,
        )
