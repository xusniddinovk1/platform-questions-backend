from __future__ import annotations
from typing import Iterable
from rest_framework import serializers
from apps.questions.models.question import Question
from apps.questions.repositories.question import QuestionRepository


class QuestionService:
    def __init__(self, repo: QuestionRepository) -> None:
        self.repo = repo

    def list_questions(self) -> Iterable[Question]:
        return self.repo.list()

def _contents_queryset() -> QuerySet[QuestionContent]:
    return QuestionContent.objects.select_related("content").only(
        *QUESTION_CONTENT_ONLY_FIELDS
    )

    def get_question(self, question_id: int) -> Question:
        question = self.repo.get(question_id)
        if not question:
            raise serializers.ValidationError({"question": "Question topilmadi."})
        return question
