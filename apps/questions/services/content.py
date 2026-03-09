from typing import Iterable
from apps.questions.models.content import Content
from apps.questions.repositories.content import ContentRepository
from apps.questions.exception.domainError import InvalidUpdatePayload, ContentNotFound
from apps.core.logger import get_logger_service

logger = get_logger_service(__name__)


class ContentService:
    def __init__(self, repo: ContentRepository) -> None:
        self.repo = repo

    def list_contents(self) -> Iterable[Content]:
        logger.info("Listing all contents")
        return self.repo.get_all()

    def get_content(self, content_id: int) -> Content:
        content = self.repo.get_by_id(content_id)
        if not content:
            logger.warning(
                "Content not found",
                extra={"content_id": content_id}
            )
            raise ContentNotFound()
        return content

    def create_content(self, content: Content) -> Content:
        logger.info(
            "Creating new content",
            extra={"content_id": getattr(content, 'id', None)}
        )
        self.repo.add(content)
        return content

    def update_content(self, content_id: int, data: dict) -> Content:
        content = self.get_content(content_id)
        if not data:
            logger.warning(
                "Invalid update payload",
                extra={"content_id": content_id, "payload": data}
            )
            raise InvalidUpdatePayload()
        for key, value in data.items():
            setattr(content, key, value)
        try:
            self.repo.update(content)
            logger.info(
                "Content updated",
                extra={"content_id": content_id}
            )
        except Exception as e:
            logger.error(
                "Error updating content",
                extra={"content_id": content_id, "error": str(e)}
            )
            raise
        return content

    def delete_content(self, content_id: int) -> None:
        try:
            self.repo.delete(content_id)
            logger.info(
                "Content deleted",
                extra={"content_id": content_id}
            )
        except Exception as e:
            logger.error(
                "Error deleting content",
                extra={"content_id": content_id, "error": str(e)}
            )
            raise