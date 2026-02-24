from django.db.models import QuerySet
from apps.questions.models.question import Question


class QuestionRepository:
    def create(self, **data: object)     -> Question:
        return Question.objects.create(**data)

    def list(self) -> QuerySet[Question]:
        return (
            Question.objects
            .all()
            .prefetch_related("contents__content")
            .order_by("-id")
        )

    def get(self, id: int) -> Question:
        return Question.objects.prefetch_related(
            "contents__content"
        ).get(id=id)

    def update(self, question: Question) -> Question:
        question.save()
        return question

    def delete(self, question: Question) -> None:
        question.delete()
