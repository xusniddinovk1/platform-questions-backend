from __future__ import annotations

from typing import cast

from django.db.models import Count, Prefetch, QuerySet
from rest_framework import viewsets
from rest_framework.serializers import Serializer
from apps.auth.permissions import IsAdminOrReadOnly
from apps.questions.models.question import Question, QuestionContent
from apps.questions.serializers.question import (
    QuestionCreateUpdateSerializer,
    QuestionSerializer
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
