from typing import Optional

from apps.core.abstructs.repository import ReadRepository, WriteRepository
from apps.questions.models.answer import Answer


class AnswerRepository(ReadRepository[Answer], WriteRepository[Answer]):

    def get_by_id(self, entity_id: int) -> Optional[Answer]:
        return (
            Answer.objects.select_related("content", "user", "question")
            .filter(id=entity_id)
            .first()
        )

    def get_all(self) -> list[Answer]:
        return list(Answer.objects.select_related("content", "user", "question").all())

    def add(self, entity: Answer) -> None:
        entity.save()

    def update(self, entity: Answer) -> None:
        entity.save()

    def delete(self, entity_id: int) -> None:
        Answer.objects.filter(id=entity_id).delete()
