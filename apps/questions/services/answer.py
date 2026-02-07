from __future__ import annotations
from typing import Final, cast
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from apps.questions.models.answer import Answer
from apps.questions.serializers.answer import AnswerCreateSerializer

ANSWER_ONLY_FIELDS: Final[tuple[str, ...]] = (
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


def base_answers_queryset() -> QuerySet[Answer]:
    return (
        Answer.objects.select_related("question", "user", "content")
        .only(*ANSWER_ONLY_FIELDS)
    )


def answers_queryset_for_request(request: Request) -> QuerySet[Answer]:
    """
    Staff -> hammasi
    Oddiy user -> faqat o'ziniki
    Anonim -> bo'sh
    """
    qs = base_answers_queryset()

    user = request.user
    if not user.is_authenticated:
        return qs.none()

    db_user = cast(AbstractBaseUser, user)

    if getattr(db_user, "is_staff", False):
        return qs

    return qs.filter(user_id=db_user.pk)


def create_answer(request: Request) -> Answer:
    ser: Serializer = AnswerCreateSerializer(
        data=request.data,
        context={"request": request},
    )
    ser.is_valid(raise_exception=True)
    return cast(Answer, ser.save())
