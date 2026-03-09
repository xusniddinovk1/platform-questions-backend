from typing import Iterable, Any
from apps.questions.models.question import Question
from apps.questions.repositories.question import QuestionRepository
from apps.questions.exception.domainError import QuestionNotFound, InvalidUpdatePayload
from apps.core.logger import get_logger_service

logger = get_logger_service(__name__)


class QuestionService:
    def __init__(self, repo: QuestionRepository) -> None:
        self.repo = repo

    def list_questions(self) -> Iterable[Question]:
        logger.info("Listing all questions")
        return self.repo.get_all()

    def get_question(self, question_id: int) -> Question:
        question = self.repo.get_by_id(question_id)
        if not question:
            logger.warning(
                "Question not found",
                extra={"question_id": question_id}
            )
            raise QuestionNotFound()
        return question

    def partial_update_question(self, pk: int, data: dict[str, Any]) -> Question:
        question = self.get_question(pk)

        allowed_fields = {
            "title",
            "start_deadline",
            "end_deadline"
        }

        payload = {k: v for k, v in data.items() if k in allowed_fields}
        if not payload:
            logger.warning(
                "Invalid update payload",
                extra={"question_id": pk, "payload": data}
            )
            raise InvalidUpdatePayload()

        for key, value in payload.items():
            setattr(question, key, value)

        try:
            self.repo.update(question)
            logger.info(
                "Question updated",
                extra={"question_id": pk}
            )
        except Exception as e:
            logger.error(
                "Error updating question",
                extra={"question_id": pk, "error": str(e)}
            )
            raise

        return question