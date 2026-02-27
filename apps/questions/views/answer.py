from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.questions.container import get_answer_service
from apps.questions.serializers.answer import AnswerSerializer, AnswerCreateSerializer
from apps.questions.services.answer import (
    AnswerAlreadyExists,
    AnswerTypeNotAllowed,
    CreateAnswerCommand,
)
from apps.questions.swagger.answer import create_answer_schema


class AnswerCreateAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @create_answer_schema
    def post(self, request: Request) -> Response:
        serializer = AnswerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = request.user.id

        if user_id is None:
            raise ValidationError({"detail": "User not found"})

        cmd = CreateAnswerCommand(
            question_id=serializer.validated_data["question_id"],
            user_id=user_id,
            content_type=serializer.validated_data["content"]["content_type"],
            payload=serializer.validated_data["content"],
        )
        try:
            answer = get_answer_service().create_answer(cmd)

            return Response(
                AnswerSerializer(answer).data,
                status=status.HTTP_201_CREATED,
            )

        except AnswerAlreadyExists:
            raise ValidationError({"detail": "Siz allaqachon javob bergansiz."})

        except AnswerTypeNotAllowed as e:
            raise ValidationError(
                {
                    "detail": (
                        f"Ruxsat etilgan turlar: {e.allowed}. "
                        f"Siz yubordingiz: {e.sent}"
                    )
                }
            )
