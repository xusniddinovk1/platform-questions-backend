from __future__ import annotations
from typing import Final, cast
from django.db.models import Count, Prefetch, QuerySet
from apps.questions.models.question import Question, QuestionContent

QUESTION_CONTENT_ONLY_FIELDS: Final[tuple[str, ...]] = (
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


def _contents_queryset() -> QuerySet[QuestionContent]:
    return QuestionContent.objects.select_related("content").only(
        *QUESTION_CONTENT_ONLY_FIELDS
    )


def build_questions_queryset() -> QuerySet[Question]:
    """
    List/Retrieve uchun optimal queryset:
    - answers_count annotate
    - contents -> content ni prefetch qilib, keraksiz fieldlarni kesadi
    """
    qs = (
        Question.objects.all()
        .annotate(answers_count=Count("answers"))
        .prefetch_related(Prefetch("contents", queryset=_contents_queryset()))
    )
    return cast(QuerySet[Question], qs)
