import math
from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional, Sequence, cast
from django.db.models import (
    BooleanField,
    Count,
    ExpressionWrapper,
    OuterRef,
    Q,
    Exists
)
from django.utils import timezone
from apps.core.abstructs.repository.read import ReadRepository
from apps.core.abstructs.repository.write import WriteRepository
from apps.questions.models.question import Question, QuestionContent
# QuestionContent modeli nomini o'zingizniki bilan tekshiring
from apps.questions.models.content import ContentRole, ContentType


@dataclass
class PaginatedResult:
    items: Sequence[Question]
    total: int
    page: int
    limit: int

    @property
    def total_pages(self) -> int:
        if self.limit <= 0:
            return 0
        return math.ceil(self.total / self.limit)


class QuestionRepository(ReadRepository[Question], WriteRepository[Question]):

    def get_by_id(self, entity_id: int) -> Optional[Question]:
        return (
            Question.objects.filter(id=entity_id)
            .select_related("category")
            .prefetch_related("contents__content", "answers")  # type: ignore[misc]
            .first()
        )

    def get_all(self) -> List[Question]:
        return list(
            Question.objects.all()
            .select_related("category")
            .prefetch_related("contents__content", "answers")  # type: ignore[misc]
            .order_by("-id")
        )

    def get_paginated(
            self,
            page: int = 1,
            limit: int = 10,
            category_id: Optional[int] = None
    ) -> PaginatedResult:
        now = timezone.now()
        three_days_ago = now - timedelta(days=3)

        queryset = Question.objects.annotate(
            success_count=Count('answers', filter=Q(answers__is_correct=True)),
            failed_count=Count('answers', filter=Q(answers__is_correct=False)),

            is_new_calc=ExpressionWrapper(
                Q(created_at__gte=three_days_ago),
                output_field=BooleanField()
            ),

            has_image_content=Exists(
                QuestionContent.objects.filter(
                    question_id=OuterRef('pk'),
                    role=ContentRole.OPTION,
                    content__content_type=ContentType.IMAGE
                )
            )
        ).select_related("category").prefetch_related(
            "contents__content",
            "answers"  # type: ignore[misc]
        ).order_by("-id")

        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)

        total = queryset.count()
        offset = (page - 1) * limit

        items_list = list(queryset[offset: offset + limit])

        items = cast(Sequence[Question], items_list)

        return PaginatedResult(
            items=items,
            total=total,
            page=page,
            limit=limit,
        )

    def add(self, entity: Question) -> None:
        entity.save()

    def update(self, entity: Question) -> None:
        entity.save()

    def delete(self, entity_id: int) -> None:
        Question.objects.filter(id=entity_id).delete()
