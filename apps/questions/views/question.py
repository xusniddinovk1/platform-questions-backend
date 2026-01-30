from __future__ import annotations

from typing import cast, Any

from django.db.models import Count, Prefetch, QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from apps.auth.permissions import IsAdminOrReadOnly
from apps.questions.models.question import Question, QuestionContent
from apps.questions.serializers.question import (
    QuestionCreateUpdateSerializer,
    QuestionSerializer,
)
from apps.questions.swagger.question import (
    question_list_response_schema,
    question_response_schema,
    question_create_update_request_schema
)


class QuestionViewSet(viewsets.ModelViewSet):  # type: ignore[type-arg]
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self) -> QuerySet[Question]:
        contents_qs = QuestionContent.objects.select_related("content").only(
            "id",
            "question_id",
            "content_id",
            "role",
            "order",
            "content__id",
            "content__content_type",
            "content__text",
            "content__file",
            "content__created_at",
        )

        return cast(
            QuerySet[Question],
            Question.objects.all()
            .annotate(answers_count=Count("answers"))
            .prefetch_related(Prefetch("contents", queryset=contents_qs)),
        )

    def get_serializer_class(self) -> type[Serializer]:  # type: ignore[type-arg]
        if self.action in {"create", "update", "partial_update"}:
            return QuestionCreateUpdateSerializer
        return QuestionSerializer

    @swagger_auto_schema(
        operation_summary="Question yaratish",
        request_body=question_create_update_request_schema,
        responses={
            201: openapi.Response(
                description="Created", schema=question_response_schema

            ),
            400: "Validation error",
        },
        tags=["Questions"],
    )
    def create(self, request, *args: Any, **kwargs: Any):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Question yangilash (PUT)",
        request_body=question_create_update_request_schema,
        responses={
            200: openapi.Response(
                description="OK", schema=question_response_schema
            ),
            400: "Validation error",
            404: "Not found",
        },
        tags=["Questions"],
    )
    def update(self, request, *args: Any, **kwargs: Any) -> Response:
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Question qisman yangilash (PATCH)",
        request_body=question_create_update_request_schema,
        responses={
            200: openapi.Response(
                description="OK", schema=question_response_schema
            ),
            400: "Validation error",
            404: "Not found",
        },
        tags=["Questions"],
    )
    def partial_update(self, request, *args: Any, **kwargs: Any) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Questionlar ro'yxati",
        responses={200: openapi.Response(
            description="OK", schema=question_list_response_schema
        )},
        tags=["Questions"],
    )
    def list(self, request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Bitta question olish",
        responses={200: openapi.Response(
            description="OK", schema=question_response_schema
        )},
        tags=["Questions"],
    )
    def retrieve(self, request, *args: Any, **kwargs: Any) -> Response:
        return super().retrieve(request, *args, **kwargs)
