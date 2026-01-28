from typing import cast
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import QuerySet
from requests import Response
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from apps.questions.models.answer import Answer
from apps.questions.serializers.answer import AnswerCreateSerializer, AnswerSerializer


class AnswerViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,  # type: ignore[type-arg]
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Answer]:
        qs = Answer.objects.select_related("question", "user", "content").only(
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

        user = self.request.user
        if not user.is_authenticated:
            return qs.none()

        db_user = cast(AbstractBaseUser, user)

        if getattr(db_user, "is_staff", False):
            return qs

        return qs.filter(user_id=db_user.pk)

    def get_serializer_class(self) -> type[Serializer]:  # type: ignore[type-arg]
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
        if not request.user.is_authenticated:
            return Response([], status=200)

        db_user = cast(AbstractBaseUser, request.user)
        qs = self.get_queryset().filter(user_id=db_user.pk)

        page = self.paginate_queryset(qs)
        if page is not None:
            ser = AnswerSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(ser.data)

        ser = AnswerSerializer(qs, many=True, context={"request": request})
        return Response(ser.data)
