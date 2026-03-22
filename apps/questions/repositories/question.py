from typing import List, Optional, Sequence, Tuple
from django.db.models import QuerySet, Prefetch
from apps.questions.models.question import Question, QuestionContent


class QuestionRepository:
    def get_queryset(self) -> QuerySet[Question]:
        return Question.objects.prefetch_related(
            Prefetch(
                "contents",
                queryset=QuestionContent.objects.select_related("content"),
                to_attr="contents_cache"
            ),
            "answers", # type: ignore[misc]
            "category"
        )


    def get_by_id(self, entity_id: int) -> Optional[Question]:
        return (
            self.get_queryset()
            .select_related("category")
            .prefetch_related("contents__content", "answers") # type: ignore[misc]
            .filter(id=entity_id)
            .first()
        )


    def get_all(self) -> List[Question]:
        return list(
            self.get_queryset()
            .select_related("category")
            .prefetch_related("contents__content", "answers") # type: ignore[misc]
            .order_by("-id")
        )


    def filter_by_category(self, category_id: int) -> QuerySet[Question]:
        return self.get_queryset().filter(category_id=category_id)


    def get_paginated(
            self,
            page: int = 1,
            limit: int = 10,
            category_id: Optional[int] = None,
    ) -> Tuple[Sequence[Question], int]:
        queryset = self.get_queryset().order_by("-id")

        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)

        total = queryset.count()
        offset = (page - 1) * limit

        items = list(queryset[offset: offset + limit])

        return items, total


    def add(self, entity: Question) -> Question:
        entity.save()
        return entity


    def update(self, entity: Question) -> Question:
        entity.save()
        return entity


    def delete(self, entity_id: int) -> None:
        Question.objects.filter(id=entity_id).delete()
