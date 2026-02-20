from __future__ import annotations
from rest_framework import status
from apps.questions.exception.base_exceptions import QuestionsBaseException


class AnswerNotFound(QuestionsBaseException):
    status_code: int = status.HTTP_404_NOT_FOUND
    default_detail = "Answer not found."
    default_code = "answer_not_found"
