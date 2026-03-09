from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.questions.container import get_answer_service
from apps.questions.serializers.answer import AnswerCreateSerializer, AnswerSerializer
from apps.questions.services.answer import (
    CreateAnswerCommand,
    AnswerAlreadyExists,
    AnswerTypeNotAllowed,
)
from apps.questions.swagger.answer import create_answer_schema
from apps.core.responses import build_success_response, build_error_response


class AnswerCreateAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @create_answer_schema
    def post(self, request: Request) -> Response:
        serializer = AnswerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = request.user.id
        if not user_id:
            return build_error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                code="USER_NOT_FOUND",
                title="User not found",
                detail="Current user not found"
            )

        cmd = CreateAnswerCommand(
            question_id=serializer.validated_data["question_id"],
            user_id=user_id,
            content_type=serializer.validated_data["content"]["content_type"],
            payload=serializer.validated_data["content"],
        )

        service = get_answer_service()

        try:
            answer = service.create_answer(cmd)

            return build_success_response(
                data=AnswerSerializer(answer).data,
                status_code=status.HTTP_201_CREATED
            )

        except AnswerAlreadyExists:
            return build_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                code="ANSWER_ALREADY_EXISTS",
                title="Answer already exists",
                detail="Siz allaqachon javob bergansiz."
            )

        except AnswerTypeNotAllowed as e:
            return build_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                code="ANSWER_TYPE_NOT_ALLOWED",
                title="Answer type not allowed",
                detail=f"Ruxsat etilgan turlar: {e.allowed}. Siz yubordingiz: {e.sent}"
            )
