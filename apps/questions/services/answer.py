from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable
from django.db import IntegrityError, transaction
from rest_framework import serializers
from apps.questions.models.answer import Answer
from apps.questions.models.question import Question
from apps.questions.models.mics import Content
from apps.questions.serializers.mics import ContentSerializer
from apps.questions.repositories.answer import AnswerRepository
from apps.questions.repositories.question import QuestionRepository


class DomainError(Exception):
    """Service layer uchun umumiy xatolik."""


class AnswerAlreadyExists(DomainError):
    pass


class AnswerTypeNotAllowed(DomainError):
    def __init__(self, allowed: list[str], sent: str) -> None:
        self.allowed = allowed
        self.sent = sent
        super().__init__(f"Allowed: {allowed}. Sent: {sent}")


@dataclass(frozen=True)
class CreateAnswerCommand:
    question_id: int
    user_id: int
    content: dict[str, Any]


class AnswerService:
    def __init__(
            self,
            question_repo: QuestionRepository,
            answer_repo: AnswerRepository,
    ) -> None:
        self.question_repo = question_repo
        self.answer_repo = answer_repo

    def _get_question_or_404(self, question_id: int) -> Question:
        question = self.question_repo.get(question_id)
        if not question:
            raise serializers.ValidationError({"question": "Question topilmadi."})
        return question

    def ensure_answer_type_allowed(self, question: Question, content_type: str) -> None:
        allowed = list(question.allowed_answer_types or [])
        if allowed and content_type not in allowed:
            raise AnswerTypeNotAllowed(allowed=allowed, sent=content_type)

    @transaction.atomic
    def create_answer(self, cmd: CreateAnswerCommand) -> Answer:
        question = self._get_question_or_404(cmd.question_id)

        content_type = cmd.content.get("content_type")
        if not content_type:
            raise serializers.ValidationError({"content": {"content_type": "Majburiy."}})

        self.ensure_answer_type_allowed(question, content_type)
        self.ensure_not_answered_yet(question, cmd.user_id)

        # Content create (serializer orqali)
        content_ser = ContentSerializer(data=cmd.content)
        content_ser.is_valid(raise_exception=True)
        content_obj: Content = content_ser.save()

        try:
            return self.answer_repo.create(
                question=question,
                user_id=cmd.user_id,
                content=content_obj,
            )
        except IntegrityError:
            # race condition bo'lsa ham constraint ushlab qoladi
            raise AnswerAlreadyExists("User already answered this question.")
