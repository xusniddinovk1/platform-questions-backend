from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from apps.questions.container import get_question_service
from apps.questions.serializers.question import QuestionSerializer
from apps.core.responses import (
    build_success_response,
    build_error_response,
    Meta,
    PaginationMeta,
)
from apps.questions.services.question import (
    QuestionNotFound,
    InvalidUpdatePayload,
    ListQuestionsQuery,
)
from apps.questions.swagger.question import (
    questions_list_schema,
    get_question_by_id_schema,
)
from apps.core.logger import LoggerType, get_logger_service


class QuestionListAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    log: LoggerType

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)
        self.log = get_logger_service(__name__)

    @questions_list_schema
    def get(self, request: Request) -> Response:
        # --- Query params o'qish ---
        try:
            page = int(request.query_params.get("page", 1))
            limit = int(request.query_params.get("limit", 10))
        except (ValueError, TypeError):
            return build_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                code="INVALID_QUERY_PARAMS",
                title="Invalid query params",
                detail="page va limit butun son bo'lishi kerak",
            )

        category_id_raw = request.query_params.get("category_id")
        category_id = None
        if category_id_raw is not None:
            try:
                category_id = int(category_id_raw)
            except (ValueError, TypeError):
                return build_error_response(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    code="INVALID_QUERY_PARAMS",
                    title="Invalid query params",
                    detail="category_id butun son bo'lishi kerak",
                )

        query = ListQuestionsQuery(page=page, limit=limit, category_id=category_id)

        service = get_question_service()
        result = service.list_questions_paginated(query)

        self.log.info(
            f"Fetched {len(result.items)} questions "
            f"(page={result.page}, limit={result.limit}, total={result.total})"
        )

        data = QuestionSerializer(result.items, many=True).data

        pagination: PaginationMeta = {
            "page": result.page,
            "limit": result.limit,
            "total": result.total,
            "totalPages": result.total_pages,
        }
        meta: Meta = {"pagination": pagination}

        return build_success_response(data=data, meta=meta)


class QuestionDetailAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    log: LoggerType

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)
        self.log = get_logger_service(__name__)

    @get_question_by_id_schema
    def get(self, request: Request, pk: int) -> Response:
        service = get_question_service()
        try:
            question = service.get_question(pk)
            self.log.info(f"Question with id={pk} fetched successfully")
            return build_success_response(data=QuestionSerializer(question).data)
        except QuestionNotFound:
            self.log.warning(f"Question with id={pk} not found")
            return build_error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                code="QUESTION_NOT_FOUND",
                title="Question not found",
                detail=f"Question with id {pk} does not exist",
            )

    def patch(self, request: Request, pk: int) -> Response:
        if not isinstance(request.data, dict):
            self.log.error("Invalid JSON body for patch request")
            raise ValidationError({"detail": "Body JSON object bo'lishi kerak."})

        service = get_question_service()
        try:
            updated = service.partial_update_question(pk, request.data)
            self.log.info(f"Question with id={pk} updated successfully")
            return build_success_response(data=QuestionSerializer(updated).data)
        except QuestionNotFound:
            self.log.warning(f"Attempted to update non-existent question id={pk}")
            return build_error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                code="QUESTION_NOT_FOUND",
                title="Question not found",
                detail=f"Question with id {pk} does not exist",
            )
        except InvalidUpdatePayload:
            self.log.warning(f"Invalid update payload for question id={pk}")
            return build_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                code="INVALID_UPDATE_PAYLOAD",
                title="Invalid update payload",
                detail="Yangilash uchun ma'lumot yuborilmadi",
            )
