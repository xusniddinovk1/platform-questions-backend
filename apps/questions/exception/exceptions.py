from __future__ import annotations

from rest_framework.exceptions import APIException
from rest_framework import status


class QuestionsBaseException(APIException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    default_detail = "Questions service error."
    default_code = "questions_error"


class PermissionDeniedForAction(QuestionsBaseException):
    status_code: int = status.HTTP_403_FORBIDDEN
    default_detail = "You don't have permission to perform this action."
    default_code = "permission_denied"


class QuestionNotFound(QuestionsBaseException):
    status_code: int = status.HTTP_404_NOT_FOUND
    default_detail = "Question not found."
    default_code = "question_not_found"


class AnswerNotFound(QuestionsBaseException):
    status_code: int = status.HTTP_404_NOT_FOUND
    default_detail = "Answer not found."
    default_code = "answer_not_found"
