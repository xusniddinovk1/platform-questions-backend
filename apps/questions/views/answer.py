from __future__ import annotations

from django.db.models import QuerySet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from apps.questions.models.answer import Answer
from apps.questions.serializers.answer import AnswerCreateSerializer, AnswerSerializer
from apps.questions.services.answer import (
    answers_queryset_for_request,
    create_answer,
)


class AnswerViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,  # type: ignore[type-arg]
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Answer]:
        return answers_queryset_for_request(self.request)

    def get_serializer_class(self) -> type[Serializer]:  # type: ignore[type-arg]
        if self.action == "create":
            return AnswerCreateSerializer
        return AnswerSerializer

    def create(
            self,
            request: Request,
            *args: object,
            **kwargs: object,
    ) -> Response:
        answer = create_answer(request)
        out = AnswerSerializer(answer, context={"request": request})
        return Response(out.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="mine")
    def mine(self, request: Request) -> Response:
        qs = self.get_queryset()

        page = self.paginate_queryset(qs)
        if page is not None:
            ser = AnswerSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(ser.data)

        ser = AnswerSerializer(qs, many=True, context={"request": request})
        return Response(ser.data)
