from __future__ import annotations
from dataclasses import dataclass
from django.db import transaction
from apps.questions.exception.domainError import (
    DomainError,
    QuestionNotFound,
    InvalidContentType,
    AnswerAlreadyExists,
)
from apps.questions.models.answer import Answer
from apps.questions.models.question import Question
from apps.questions.models.content import Content
from apps.questions.repositories.answer import AnswerRepository
from apps.questions.repositories.content import ContentRepository
from apps.questions.repositories.question import QuestionRepository
import logging

logger = logging.getLogger(__name__)


# Custom error for type not allowed
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
    payload: dict


class AnswerService:
    def __init__(
            self,
            question_repo: QuestionRepository,
            answer_repo: AnswerRepository,
            content_repo: ContentRepository,
    ) -> None:
        self.question_repo = question_repo
        self.answer_repo = answer_repo
        self.content_repo = content_repo

    def _get_question(self, question_id: int) -> Question:
        question = self.question_repo.get_by_id(question_id)
        if not question:
            raise QuestionNotFound()
        return question


    @transaction.atomic
    def create_answer(self, cmd: CreateAnswerCommand) -> Answer:
        logger.info(
            "Creating answer",
            extra={
                "question_id": cmd.question_id,
                "user_id": cmd.user_id,
                "content_type": cmd.content_type
            },
        )

        question = self._get_question(cmd.question_id)

        if not cmd.content_type:
            raise InvalidContentType("content_type is required")


        # Create content
        content_obj = Content(
            content_type=cmd.content_type,
            text=cmd.payload.get("text"),
            file=cmd.payload.get("file"),
        )
        self.content_repo.add(content_obj)

        # Check if user already answered
        existing = Answer.objects.filter(question=question, user_id=cmd.user_id).first()
        if existing:
            raise AnswerAlreadyExists("User already answered this question.")

        answer = Answer(
            question=question,
            user_id=cmd.user_id,
            content=content_obj
        )
        self.answer_repo.add(answer)
        return answer
