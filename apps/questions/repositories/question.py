from typing import Optional, List
from apps.core.abstructs.repository.read import ReadRepository
from apps.core.abstructs.repository.write import WriteRepository
from apps.questions.models.question import Question


class QuestionRepository(ReadRepository[Question], WriteRepository[Question]):

    def get_by_id(self, entity_id: int) -> Optional[Question]:
        return (
            Question.objects.prefetch_related("contents__content")
            .filter(id=entity_id)
            .first()
        )

    def get_all(self) -> List[Question]:
        return list(
            Question.objects.all().prefetch_related("contents__content").order_by("-id")
        )

    def add(self, entity: Question) -> None:
        entity.save()

    def update(self, entity: Question) -> None:
        entity.save()

    def delete(self, entity_id: int) -> None:
        Question.objects.filter(id=entity_id).delete()
