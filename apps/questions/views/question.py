from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from apps.questions.container import get_question_service
from apps.questions.serializers.question import QuestionSerializer
from apps.core.responses import build_success_response, build_error_response
from apps.questions.services.question import QuestionNotFound, InvalidUpdatePayload
from apps.questions.swagger.question import (
    questions_list_schema,
    get_question_by_id_schema,
)


class QuestionListAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @questions_list_schema
    def get(self, request: Request) -> Response:
        service = get_question_service()
        questions = service.list_questions()

        return build_success_response(
            data=QuestionSerializer(questions, many=True).data
        )


class QuestionDetailAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @get_question_by_id_schema
    def get(self, request: Request, pk: int) -> Response:
        service = get_question_service()
        try:
            question = service.get_question(pk)
            return build_success_response(
                data=QuestionSerializer(question).data
            )
        except QuestionNotFound:
            return build_error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                code="QUESTION_NOT_FOUND",
                title="Question not found",
                detail=f"Question with id {pk} does not exist"
            )

    def patch(self, request: Request, pk: int) -> Response:
        if not isinstance(request.data, dict):
            raise ValidationError({"detail": "Body JSON object bo'lishi kerak."})

        service = get_question_service()
        try:
            updated = service.partial_update_question(pk, request.data)
            return build_success_response(
                data=QuestionSerializer(updated).data
            )
        except QuestionNotFound:
            return build_error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                code="QUESTION_NOT_FOUND",
                title="Question not found",
                detail=f"Question with id {pk} does not exist"
            )
        except InvalidUpdatePayload:
            return build_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                code="INVALID_UPDATE_PAYLOAD",
                title="Invalid update payload",
                detail="Yangilash uchun ma'lumot yuborilmadi"
            )
