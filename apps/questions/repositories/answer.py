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

    def get(self, id: int) -> Answer:
        return Answer.objects.select_related(
            "content", "user", "question"
        ).get(id=id)

    def delete(self, answer: Answer) -> None:
        answer.delete()
