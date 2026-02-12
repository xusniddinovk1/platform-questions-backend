from django.db.models import QuerySet
from apps.questions.models.answer import Answer
from apps.questions.models.question import Question
from apps.questions.models.mics import Content


class AnswerRepository:
    def create(self, question: Question, user_id: int, content: Content) -> Answer:
        return Answer.objects.create(
            question=question,
            user_id=user_id,
            content=content,
        )

    # def list_by_question(self, question: Question) -> QuerySet[Answer]:
    #     return (
    #         Answer.objects
    #         .filter(question=question)
    #         .select_related("content", "user", "question")
    #         .order_by("-id")
    #     )
    #
    # def exists_for_user(self, question: Question, user_id: int) -> bool:
    #     return Answer.objects.filter(question=question, user_id=user_id).exists()

    def get(self, id: int) -> Answer | None:
        try:
            return Answer.objects.select_related("content", "user", "question").get(id=id)
        except Answer.DoesNotExist:
            return None

    def delete(self, answer: Answer) -> None:
        answer.delete()
