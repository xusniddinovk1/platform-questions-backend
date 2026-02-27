from __future__ import annotations
from rest_framework import status
from apps.questions.exception.base_exceptions import QuestionsBaseException


class PermissionDeniedForAction(QuestionsBaseException):
    status_code: int = status.HTTP_403_FORBIDDEN
    default_detail = "You don't have permission to perform this action."
    default_code = "permission_denied"
