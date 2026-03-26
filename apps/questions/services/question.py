from typing import Any
from datetime import timedelta
from django.utils import timezone
from django.db.models import QuerySet

from apps.questions.models.question import Question
from apps.questions.models.content import ContentRole, ContentType
from apps.questions.repositories.question import QuestionRepository
from apps.questions.exception.domainError import QuestionNotFound, InvalidUpdatePayload
from apps.questions.dto.question import ListQuestionsQuery


class QuestionService:
    def __init__(self, repo: QuestionRepository) -> None:
        self.repo = repo

    def get_question_type(self, obj: Question) -> str:
        all_contents = getattr(obj, "contents_cache", obj.contents.all())
        options = [c for c in all_contents if c.role == ContentRole.OPTION]

        if options:
            return "options"
        if getattr(obj, "has_image_content", False):
            return "image"
        return "text"

    def get_payload(self, obj: Question) -> dict:
        q_type = self.get_question_type(obj)
        if q_type == "text":
            return {}

        payload: dict = {}
        all_contents = getattr(obj, "contents_cache", obj.contents.all())

        if q_type == "options":
            options = [c for c in all_contents if c.role == ContentRole.OPTION]
            if options:
                from apps.questions.serializers.option import OptionSerializer
                payload["options"] = OptionSerializer(options, many=True).data

        images = [
            c.content.file.url for c in all_contents
            if c.role == ContentRole.ATTACHMENT
               and c.content.content_type == ContentType.IMAGE
               and c.content.file
        ]
        if images:
            payload["imageUrls"] = images

        return payload

    def list_questions(self,
                       query: ListQuestionsQuery
                       ) -> QuerySet[Question]:
        now = timezone.now()
        three_days_ago = now - timedelta(days=3)

        qs = self.repo.get_annotated_list(three_days_ago)

        if query.category_id:
            qs = qs.filter(category_id=query.category_id)

        return qs.order_by("-id")

    def get_question(self, question_id: int) -> Question:
        question = self.repo.get_by_id(question_id)
        if not question:
            raise QuestionNotFound()
        return question

    def partial_update_question(self,
                                pk: int,
                                data: dict[str, Any]
                                ) -> Question:
        question = self.get_question(pk)

        allowed_fields = {"title", "start_deadline", "end_deadline"}
        payload = {k: v for k, v in data.items() if k in allowed_fields}

        if not payload:
            raise InvalidUpdatePayload()

        for key, value in payload.items():
            setattr(question, key, value)

        return self.repo.update(question)

def get_questions_svc() -> QuestionService:
    repository = QuestionRepository()
    return QuestionService(repo=repository)
