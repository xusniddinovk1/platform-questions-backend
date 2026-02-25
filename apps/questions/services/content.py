from typing import Iterable
from apps.questions.models.content import Content
from apps.questions.repositories.content import ContentRepository
from apps.questions.exception.domainError import InvalidUpdatePayload, ContentNotFound


class ContentService:
    def __init__(self, repo: ContentRepository) -> None:
        self.repo = repo

    def list_contents(self) -> Iterable[Content]:
        return self.repo.get_all()

    def get_content(self, content_id: int) -> Content:
        content = self.repo.get_by_id(content_id)
        if not content:
            raise ContentNotFound()
        return content

    def create_content(self, content: Content) -> None:
        self.repo.add(content)

    def update_content(self, content_id: int, data: dict) -> Content:
        content = self.get_content(content_id)

        if not data:
            raise InvalidUpdatePayload()

        for key, value in data.items():
            setattr(content, key, value)

        self.repo.update(content)
        return content

    def delete_content(self, content_id: int) -> None:
        self.repo.delete(content_id)
