from __future__ import annotations
from rest_framework import status
from apps.questions.exception.base_exceptions import QuestionsBaseException


class QuestionNotFound(QuestionsBaseException):
    status_code: int = status.HTTP_404_NOT_FOUND
    default_detail = "Question not found."
    default_code = "question_not_found"
