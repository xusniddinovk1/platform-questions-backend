from django.db.models import QuerySet
from apps.questions.models.question import Question


class QuestionRepository:
    def create(self, question: Question) -> Question:
        question.save()
        return question

    def list(self) -> QuerySet[Question]:
        return (
            Question.objects
            .all()
            .prefetch_related("contents__content")
            .order_by("-id")
        )

    def get(self, id: int) -> Question | None:
        try:
            return Question.objects.prefetch_related("contents__content").get(id=id)
        except Question.DoesNotExist:
            return None

    def update(self, question: Question) -> Question:
        question.save()
        return question

    def delete(self, question: Question) -> None:
        question.delete()
