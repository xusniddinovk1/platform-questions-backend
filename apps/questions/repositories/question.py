from typing import List, Optional
from apps.core.abstructs.repository.read import ReadRepository
from apps.core.abstructs.repository.write import WriteRepository
from apps.questions.models.question import Question
from apps.core.logger import get_logger_service

logger = get_logger_service(__name__)


class QuestionRepository(ReadRepository[Question], WriteRepository[Question]):

    def get_by_id(self, entity_id: int) -> Optional[Question]:
        try:
            queryset = (
                Question.objects
                .select_related("category")
                .prefetch_related(
                    "contents__content",
                    "answers"
                )
            )
            return queryset.filter(id=entity_id).first()
        except Exception as e:
            logger.error(
                "Error fetching Question by id",
                extra={"question_id": entity_id, "error": str(e)}
            )
            raise

    def get_all(self) -> List[Question]:
        try:
            return list(
                Question.objects
                .all()
                .prefetch_related("contents__content")
                .order_by("-id")
            )
        except Exception as e:
            logger.error("Error fetching all Questions", extra={"error": str(e)})
            raise

    def add(self, entity: Question) -> None:
        try:
            entity.save()
            logger.info("Question created", extra={"question_id": entity.id})
        except Exception as e:
            logger.error(
                "Error creating Question",
                extra={"question_id": getattr(entity, 'id', None), "error": str(e)}
            )
            raise

    def update(self, entity: Question) -> None:
        try:
            entity.save()
            logger.info("Question updated", extra={"question_id": entity.id})
        except Exception as e:
            logger.error(
                "Error updating Question",
                extra={"question_id": entity.id, "error": str(e)}
            )
            raise

    def delete(self, entity_id: int) -> None:
        try:
            Question.objects.filter(id=entity_id).delete()
            logger.info("Question deleted", extra={"question_id": entity_id})
        except Exception as e:
            logger.error(
                "Error deleting Question",
                extra={"question_id": entity_id, "error": str(e)}
            )
            raise