from typing import Iterable, Any, Optional
from dataclasses import dataclass
from apps.questions.models.question import Question
from apps.questions.repositories.question import QuestionRepository, PaginatedResult
from apps.questions.exception.domainError import QuestionNotFound, InvalidUpdatePayload


@dataclass
class ListQuestionsQuery:
    page: int = 1
    limit: int = 10
    category_id: Optional[int] = None


class QuestionService:
    def __init__(self, repo: QuestionRepository) -> None:
        self.repo = repo

    def list_questions(self) -> Iterable[Question]:
        return self.repo.get_all()

    def list_questions_paginated(self, query: ListQuestionsQuery) -> PaginatedResult:
        page = max(1, query.page)
        limit = min(max(1, query.limit), 100)  # max 100 ta limit
        return self.repo.get_paginated(
            page=page,
            limit=limit,
            category_id=query.category_id,
        )

    def get_question(self, question_id: int) -> Question:
        question = self.repo.get_by_id(question_id)
        if not question:
            raise QuestionNotFound()
        return question

    def partial_update_question(self, pk: int, data: dict[str, Any]) -> Question:
        question = self.get_question(pk)

        allowed_fields = {"title", "start_deadline", "end_deadline"}

        payload = {k: v for k, v in data.items() if k in allowed_fields}
        if not payload:
            raise InvalidUpdatePayload()

        for key, value in payload.items():
            setattr(question, key, value)

        self.repo.update(question)

        return question
