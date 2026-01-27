from __future__ import annotations

from typing import Any, Type

from django.db.models import Count, Prefetch, QuerySet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from .models import Answer, Question, QuestionContent
from .permissions import IsAdminOrReadOnly
from .serializers import (
    AnswerCreateSerializer,
    AnswerSerializer,
    QuestionCreateUpdateSerializer,
    QuestionSerializer,
)


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self) -> QuerySet[Question]:
        contents_qs = (
            QuestionContent.objects.select_related("content")
            .only(
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
        )

        return (
            Question.objects.all()
            .annotate(answers_count=Count("answers"))
            .prefetch_related(Prefetch("contents", queryset=contents_qs))
        )

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action in {"create", "update", "partial_update"}:
            return QuestionCreateUpdateSerializer
        return QuestionSerializer


class AnswerViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Answer]:
        qs = (
            Answer.objects.select_related("question", "user", "content")
            .only(
                "id",
                "question_id",
                "user_id",
                "content_id",
                "created_at",
                "question__id",
                "question__title",
                "user__id",
                "content__id",
                "content__content_type",
                "content__text",
                "content__file",
                "content__created_at",
            )
        )

        user = self.request.user
        if user.is_staff:
            return qs
        return qs.filter(user=user)

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action == "create":
            return AnswerCreateSerializer
        return AnswerSerializer

    def create(
            self,
            request: Request,
            *args: tuple[object, ...],
            **kwargs: dict[str, object],
    ) -> Response:
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        answer: Answer = serializer.save()

        out = AnswerSerializer(answer, context={"request": request})
        return Response(out.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="mine")
    def mine(self, request: Request) -> Response:
        qs = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = AnswerSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(ser.data)

        ser = AnswerSerializer(qs, many=True, context={"request": request})
        return Response(ser.data)
