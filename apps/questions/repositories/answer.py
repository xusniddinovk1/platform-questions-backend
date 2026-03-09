from typing import Optional, List
from apps.core.abstructs.repository import ReadRepository, WriteRepository
from apps.questions.models.answer import Answer
from apps.core.logger import get_logger_service

logger = get_logger_service(__name__)


class AnswerRepository(ReadRepository[Answer], WriteRepository[Answer]):

    def get_by_id(self, entity_id: int) -> Optional[Answer]:
        try:
            return (
                Answer.objects
                .select_related("user", "question")
                .prefetch_related("selected_options")
                .filter(id=entity_id)
                .first()
            )
        except Exception as e:
            logger.error(
                "Error fetching Answer by id",
                extra={"answer_id": entity_id, "error": str(e)}
            )
            raise

    def get_all(self) -> List[Answer]:
        try:
            return list(
                Answer.objects
                .select_related("user", "question")
                .prefetch_related("selected_options")
                .all()
            )
        except Exception as e:
            logger.error("Error fetching all Answers", extra={"error": str(e)})
            raise

    def add(self, entity: Answer) -> None:
        try:
            entity.save()
            logger.info("Answer created", extra={"answer_id": entity.id})
        except Exception as e:
            logger.error(
                "Error creating Answer",
                extra={"answer_id": getattr(entity, 'id', None), "error": str(e)}
            )
            raise

    def update(self, entity: Answer) -> None:
        try:
            entity.save()
            logger.info("Answer updated", extra={"answer_id": entity.id})
        except Exception as e:
            logger.error(
                "Error updating Answer",
                extra={"answer_id": entity.id, "error": str(e)}
            )
            raise

    def delete(self, entity_id: int) -> None:
        try:
            Answer.objects.filter(id=entity_id).delete()
            logger.info("Answer deleted", extra={"answer_id": entity_id})
        except Exception as e:
            logger.error(
                "Error deleting Answer",
                extra={"answer_id": entity_id, "error": str(e)}
            )
            raise