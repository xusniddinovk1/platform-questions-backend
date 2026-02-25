from typing import Optional, List
from apps.core.abstructs.repository.read import ReadRepository
from apps.core.abstructs.repository.write import WriteRepository
from apps.questions.models.content import Content


class ContentRepository(ReadRepository[Content], WriteRepository[Content]):

    def get_by_id(self, entity_id: int) -> Optional[Content]:
        return Content.objects.filter(id=entity_id).first()

    def get_all(self) -> List[Content]:
        return list(Content.objects.all())

    def add(self, entity: Content) -> None:
        entity.save()

    def update(self, entity: Content) -> None:
        entity.save()

    def delete(self, entity_id: int) -> None:
        Content.objects.filter(id=entity_id).delete()
