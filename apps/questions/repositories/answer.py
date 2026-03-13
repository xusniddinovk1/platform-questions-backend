from typing import Optional, List
from apps.core.abstructs.repository import ReadRepository, WriteRepository
from apps.questions.models.answer import Answer


class AnswerRepository(ReadRepository[Answer], WriteRepository[Answer]):

    def get_by_id(self, entity_id: int) -> Optional[Answer]:
        return (
            Answer.objects.select_related("user", "question")
            .prefetch_related("selected_options")
            .filter(id=entity_id)
            .first()
        )

    def get_all(self) -> List[Answer]:
        return list(
            Answer.objects.select_related("user", "question")
            .prefetch_related("selected_options")
            .all()
        )

    def add(self, entity: Answer) -> None:
        entity.save()

    def update(self, entity: Answer) -> None:
        entity.save()

    def delete(self, entity_id: int) -> None:
        Answer.objects.filter(id=entity_id).delete()
