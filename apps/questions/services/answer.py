from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from django.db import IntegrityError, transaction

from apps.questions.models.answer import Answer
from apps.questions.models.question import Question
from apps.questions.models.mics import Content
from apps.questions.repositories.answer import AnswerRepository
from apps.questions.repositories.question import QuestionRepository


class DomainError(Exception):
    """Service layer uchun umumiy xatolik."""
    pass


class QuestionNotFound(DomainError):
    pass


class InvalidContentType(DomainError):
    pass


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
    content_type: str
    payload: dict[str, Any]



class AnswerService:

    def __init__(
            self,
            question_repo: QuestionRepository,
            answer_repo: AnswerRepository,
    ) -> None:
        self.question_repo = question_repo
        self.answer_repo = answer_repo

    def _get_question(self, question_id: int) -> Question:
        question = self.question_repo.get(question_id)
        if not question:
            raise QuestionNotFound()
        return question

    def ensure_answer_type_allowed(self, question: Question, content_type: str) -> None:
        allowed = list(question.allowed_answer_types or [])
        if allowed and content_type not in allowed:
            raise AnswerTypeNotAllowed(allowed=allowed, sent=content_type)

    @transaction.atomic
    def create_answer(self, cmd: CreateAnswerCommand) -> Answer:

        question = self._get_question(cmd.question_id)

        if not cmd.content_type:
            raise InvalidContentType("content_type is required")

        if self.answer_repo.exists(cmd.question_id, cmd.user_id):
            raise AnswerAlreadyExists("User already answered this question.")

        self.ensure_answer_type_allowed(question, cmd.content_type)

        content_obj = Content.objects.create(
            content_type=cmd.content_type,
            **cmd.payload
        )

        try:
            return self.answer_repo.create(
                question=question,
                user_id=cmd.user_id,
                content=content_obj,
            )
        except IntegrityError:
            raise AnswerAlreadyExists("User already answered this question.")
