from apps.questions.repositories.content import ContentRepository
from apps.questions.repositories.question import QuestionRepository
from apps.questions.repositories.answer import AnswerRepository
from apps.questions.services.question import QuestionService
from apps.questions.services.answer import AnswerService


def get_question_repository() -> QuestionRepository:
    return QuestionRepository()


def get_answer_repository() -> AnswerRepository:
    return AnswerRepository()


def get_question_service() -> QuestionService:
    return QuestionService(
        repo=get_question_repository()
    )


def get_answer_service() -> AnswerService:
    return AnswerService(
        question_repo=QuestionRepository(),
        answer_repo=AnswerRepository(),
        content_repo=ContentRepository(),
    )
