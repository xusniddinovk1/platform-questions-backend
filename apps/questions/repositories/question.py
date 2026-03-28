from typing import List, Optional, Sequence, Tuple
from datetime import datetime
from django.db.models import (
    QuerySet,
    Prefetch,
    Count, Q, Exists, OuterRef,
    BooleanField,
    ExpressionWrapper)
from apps.questions.models.question import Question, QuestionContent
from apps.questions.models.content import ContentRole, ContentType


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

    def get_annotated_list(self, new_threshold_date: datetime) -> QuerySet[Question]:
        return self.get_queryset().annotate(
            success_count=Count('answers', filter=Q(answers__is_correct=True)),
            failed_count=Count('answers', filter=Q(answers__is_correct=False)),
            is_new_calc=ExpressionWrapper(
                Q(created_at__gte=new_threshold_date),
                output_field=BooleanField()
            ),
            has_image_content=Exists(
                QuestionContent.objects.filter(
                    question_id=OuterRef('pk'),
                    role=ContentRole.OPTION,
                    content__content_type=ContentType.IMAGE
                )
            )
        )

    def get_by_id(self, entity_id: int) -> Optional[Question]:
        return self.get_queryset().filter(id=entity_id).first()

    def get_all(self) -> List[Question]:
        return list(self.get_queryset().order_by("-id"))

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
