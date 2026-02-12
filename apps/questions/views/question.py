from __future__ import annotations
from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from apps.auth.permissions import IsAdminOrReadOnly
from apps.questions.models.question import Question
from apps.questions.serializers.question import (
    QuestionCreateUpdateSerializer,
    QuestionSerializer,
)
from apps.questions.services.question import build_questions_queryset
from apps.questions.swagger.question import (
    question_create_update_request_schema,
    question_list_response_schema,
    question_response_schema,
)


class QuestionViewSet(viewsets.ModelViewSet):  # type: ignore[type-arg]
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self) -> QuerySet[Question]:
        return build_questions_queryset()

    def get_serializer_class(self) -> type[Serializer]:  # type: ignore[type-arg]
        if self.action in {"create", "update", "partial_update"}:
            return QuestionCreateUpdateSerializer
        return QuestionSerializer

    @swagger_auto_schema(
        operation_summary="Question yaratish",
        request_body=question_create_update_request_schema,
        responses={
            201: openapi.Response(description="Created", schema=question_response_schema),
        },
        tags=["Questions"],
    )
    def create(self, request: Request, *args: object, **kwargs: object) -> Response:
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Question yangilash (PUT)",
        request_body=question_create_update_request_schema,
        responses={
            200: openapi.Response(description="OK", schema=question_response_schema),
        },
        tags=["Questions"],
    )
    def update(self, request: Request, *args: object, **kwargs: object) -> Response:
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Question qisman yangilash (PATCH)",
        request_body=question_create_update_request_schema,
        responses={
            200: openapi.Response(description="OK", schema=question_response_schema),
        },
        tags=["Questions"],
    )
    def partial_update(
        self, request: Request, *args: object, **kwargs: object
    ) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Questionlar ro'yxati",
        responses={
            200: openapi.Response(description="OK", schema=question_list_response_schema),
        },
        tags=["Questions"],
    )
    def list(self, request: Request, *args: object, **kwargs: object) -> Response:
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Bitta question olish",
        responses={
            200: openapi.Response(description="OK", schema=question_response_schema),
        },
        tags=["Questions"],
    )
    def retrieve(self, request: Request, *args: object, **kwargs: object) -> Response:
        return super().retrieve(request, *args, **kwargs)
