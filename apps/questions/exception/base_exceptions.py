from __future__ import annotations
from rest_framework.exceptions import APIException
from rest_framework import status


class QuestionsBaseException(APIException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    default_detail = "Questions service error."
    default_code = "questions_error"
