from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from apps.questions.container import get_question_service
from apps.questions.swagger.question import (
    question_response_schema,
    question_list_response_schema,
)
from apps.questions.serializers.question import QuestionSerializer
from apps.questions.services.question import (
    QuestionNotFound,
    InvalidUpdatePayload,
)


class QuestionListAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_summary="Questions list",
        operation_description="Barcha savollar ro'yxatini qaytaradi",
        responses={
            200: question_list_response_schema,
        },
        tags=["Questions"],
    )
    def get(self, request: Request) -> Response:
        service = get_question_service()
        qs = service.list_questions()

        return Response(
            QuestionSerializer(qs, many=True).data,
            status=status.HTTP_200_OK,
        )


class QuestionDetailAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_summary="Get question by id",
        operation_description="Bitta questionni pk orqali qaytaradi",
        responses={
            200: question_response_schema,
            404: "Question not found",
        },
        tags=["Questions"],
    )
    def get(self, request: Request, pk: int) -> Response:
        service = get_question_service()

        try:
            question = service.get_question(pk)
            return Response(
                QuestionSerializer(question).data,
                status=status.HTTP_200_OK,
            )

        except QuestionNotFound:
            return Response(
                {"detail": "Question topilmadi."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_summary="Update question partially",
        operation_description="Savolni qisman yangilash",
        request_body=QuestionSerializer,
        responses={
            200: question_response_schema,
            400: "Invalid data",
            404: "Question not found",
        },
        tags=["Questions"],
    )
    def patch(self, request: Request, pk: int) -> Response:
        if not isinstance(request.data, dict):
            raise ValidationError({"detail": "Body JSON object bo'lishi kerak."})

        service = get_question_service()

        try:
            updated = service.partial_update_question(pk, request.data)

            return Response(
                QuestionSerializer(updated).data,
                status=status.HTTP_200_OK,
            )

        except QuestionNotFound:
            return Response(
                {"detail": "Question topilmadi."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except InvalidUpdatePayload:
            return Response(
                {"detail": "Yangilash uchun ma'lumot yuborilmadi."},
                status=status.HTTP_400_BAD_REQUEST,
            )
