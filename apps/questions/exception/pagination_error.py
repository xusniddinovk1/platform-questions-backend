from rest_framework import status
from apps.questions.exception.base_exceptions import QuestionsBaseException


class InvalidPaginationParams(QuestionsBaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Page va Limit parametrlari musbat butun son bo'lishi kerak."
    default_code = "invalid_pagination"
