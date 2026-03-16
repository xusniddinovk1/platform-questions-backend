from __future__ import annotations
from dataclasses import dataclass
from django.db import transaction

from apps.core.logger import get_logger_service
from apps.questions.exception.domainError import (
    QuestionNotFound,
    AnswerAlreadyExists,
)
from apps.questions.models.answer import Answer
from apps.questions.models.question import Question
from apps.questions.models.content import Content
from apps.questions.repositories.answer import AnswerRepository
from apps.questions.repositories.content import ContentRepository
from apps.questions.repositories.question import QuestionRepository

logger = get_logger_service(__name__)


@dataclass(frozen=True)
class CreateAnswerCommand:
    question_id: int
    user_id: int
    selected_option_ids: list[int]


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
        if question is None:
            raise QuestionNotFound(f"Question with id {question_id} not found")
        return question

    @transaction.atomic
    def create_answer(self, cmd: CreateAnswerCommand) -> Answer:
        question = self._get_question(cmd.question_id)

        if Answer.objects.filter(question=question, user_id=cmd.user_id).exists():
            logger.warning(
                f"User {cmd.user_id} tried to answer question {cmd.question_id} again"
            )
            raise AnswerAlreadyExists()

        selected_options = Content.objects.filter(
            id__in=cmd.selected_option_ids,
            questioncontent__question=question
        )
        answer = Answer(question=question, user_id=cmd.user_id)

        self.answer_repo.add(answer)
        answer.selected_options.set(selected_options)

        logger.info(
            f"Answer created for user {cmd.user_id} on question {cmd.question_id}"
        )

        return answer
