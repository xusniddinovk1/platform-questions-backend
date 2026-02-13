from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.questions.swagger.question import (
    question_response_schema,
    question_list_response_schema, question_create_update_request_schema,
)
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

    @swagger_auto_schema(
        operation_summary="Get question by id",
        operation_description="Bitta questionni pk orqali qaytaradi",
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_PATH,
                description="Question ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Question detail",
                schema=question_response_schema,
            ),
            404: openapi.Response(description="Question not found"),
        },
        tags=["Questions"],
    )
    def get(self, request: Request, pk: int) -> Response:
        question = question_service.get_question(pk)
        return Response(
            QuestionSerializer(question).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request: Request, pk: int) -> Response:
        if not isinstance(request.data, dict):
            raise ValidationError({"detail": "Body JSON object bo‘lishi kerak."})

        updated = question_service.partial_update_question(pk, request.data)
        return Response(QuestionSerializer(updated).data, status=status.HTTP_200_OK)
