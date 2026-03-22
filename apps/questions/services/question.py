from typing import Any
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q, Exists, OuterRef, BooleanField, ExpressionWrapper
from django.db.models import QuerySet
from apps.questions.models.question import Question, QuestionContent
from apps.questions.models.content import ContentRole, ContentType
from apps.questions.repositories.question import QuestionRepository
from apps.questions.exception.domainError import QuestionNotFound, InvalidUpdatePayload
from apps.questions.dto.question import ListQuestionsQuery


class QuestionService:
    def __init__(self, repo: QuestionRepository) -> None:
        self.repo = repo

    def list_questions(self, query: ListQuestionsQuery) -> QuerySet[Question]:
        now = timezone.now()
        three_days_ago = now - timedelta(days=3)

        qs = self.repo.get_queryset().annotate(
            success_count=Count('answers', filter=Q(answers__is_correct=True)), # type: ignore[misc]
            failed_count=Count('answers', filter=Q(answers__is_correct=False)), # type: ignore[misc]
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
            "answers"
        ).order_by("-id")

        if query.category_id:
            qs = qs.filter(category_id=query.category_id)

        return qs

    def get_question(self, question_id: int) -> Question:
        question = self.repo.get_by_id(question_id)
        if not question:
            raise QuestionNotFound()
        return question

    def partial_update_question(self, pk: int, data: dict[str, Any]) -> Question:
        question = self.get_question(pk)

        allowed_fields = {"title", "start_deadline", "end_deadline"}

        payload = {k: v for k, v in data.items() if k in allowed_fields}
        if not payload:
            raise InvalidUpdatePayload()

        for key, value in payload.items():
            setattr(question, key, value)

        self.repo.update(question)

        return question
