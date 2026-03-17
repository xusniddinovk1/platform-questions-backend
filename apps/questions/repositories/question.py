from typing import List, Optional
from dataclasses import dataclass
from apps.core.abstructs.repository.read import ReadRepository
from apps.core.abstructs.repository.write import WriteRepository
from apps.questions.models.question import Question


@dataclass
class PaginatedResult:
    items: List[Question]
    total: int
    page: int
    limit: int

    @property
    def total_pages(self) -> int:
        if self.limit == 0:
            return 0
        import math
        return math.ceil(self.total / self.limit)


class QuestionRepository(ReadRepository[Question], WriteRepository[Question]):

    def get_by_id(self, entity_id: int) -> Optional[Question]:
        queryset = Question.objects.select_related("category").prefetch_related(
            "contents__content", "answers"
        )  # type: ignore[misc]
        return queryset.filter(id=entity_id).first()

    def get_all(self) -> List[Question]:
        return list(
            Question.objects.all()
            .select_related("category")
            .prefetch_related("contents__content", "answers") # type: ignore[misc]
            .order_by("-id")
        )

    def get_paginated(
        self,
        page: int = 1,
        limit: int = 10,
        category_id: Optional[int] = None,
    ) -> PaginatedResult:
        queryset = (
            Question.objects.all()
            .select_related("category")
            .prefetch_related("contents__content", "answers") # type: ignore[misc]
            .order_by("-id")
        )

        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)

        total = queryset.count()

        offset = (page - 1) * limit
        items = list(queryset[offset : offset + limit])

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
