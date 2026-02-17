from __future__ import annotations
from typing import Iterable, Any
from rest_framework import serializers
from apps.questions.models.question import Question
from apps.questions.repositories.question import QuestionRepository


class QuestionService:
    def __init__(self, repo: QuestionRepository) -> None:
        self.repo = repo

    def list_questions(self) -> Iterable[Question]:
        return self.repo.list()

    def get_question(self, question_id: int) -> Question:
        question = self.repo.get(question_id)
        if not question:
            raise serializers.ValidationError({"question": "Question topilmadi."})
        return question


    def partial_update_question(self, pk: int, data: dict[str, Any]) -> Question:
        question = self.get_question(pk)

        allowed_fields = {"title", "description", "allowed_answer_types", "is_active"}
        payload = {k: v for k, v in data.items() if k in allowed_fields}

        if not payload:
            raise serializers.ValidationError({
                "detail": "Yangilash uchun field yuborilmadi."
            })

        for key, value in payload.items():
            setattr(question, key, value)

        return self.repo.update(question)
