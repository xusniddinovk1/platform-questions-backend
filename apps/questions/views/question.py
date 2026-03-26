from typing import Optional
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from apps.questions.exception.pagination_error import InvalidPaginationParams
from apps.questions.services.question import (
    QuestionNotFound,
    InvalidUpdatePayload, QuestionService, get_questions_svc,
)
from apps.questions.swagger.question import (
    get_question_by_id_schema,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from apps.questions.container import get_question_service
from apps.questions.serializers.question import QuestionSerializer
from apps.questions.services.question import ListQuestionsQuery
from apps.core.responses import (build_success_response,
                                 build_error_response,
                                 PaginationMeta)
from apps.core.logger import LoggerType, get_logger_service
from apps.questions.swagger.question import questions_list_schema


def get_clean_int(value: str | int | None, param_name: str) -> int:
    try:
        res = int(value)
        if res <= 0:
            raise ValueError
        return res
    except (ValueError, TypeError):
        raise InvalidPaginationParams(
            detail=f"{param_name} noto'g'ri formatda yoki 0 dan kichik."
        )


class QuestionListAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    log: LoggerType
    service: QuestionService

    def __init__(self,
                 service: Optional[QuestionService] = None,
                 **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)
        self.service = service or get_question_service()
        self.log = get_logger_service(__name__)

    @questions_list_schema
    def get(self, request: Request) -> Response:
        service = get_questions_svc()

        page = get_clean_int(request, "page", 1)
        limit = get_clean_int(request, "limit", 10)
        category_id = get_clean_int(request, "category_id")

        query = ListQuestionsQuery(category_id=category_id)
        queryset = service.list_questions(query)

        paginator = PageNumberPagination()
        paginator.page_size = limit
        paginated_qs = paginator.paginate_queryset(queryset, request)

        data = QuestionSerializer(paginated_qs, many=True).data

        total_count = queryset.count()
        pagination: PaginationMeta = {
            "page": page,
            "limit": limit,
            "total": total_count,
            "totalPages": (total_count + limit - 1) // limit,
        }

        self.log.info(f"Fetched {len(data)} questions (page={page}, limit={limit})")

        return build_success_response(data=data,
                                      meta={"pagination": pagination})


class QuestionDetailAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    log: LoggerType

    def __init__(self,
                 service: Optional[QuestionService] = None,
                 **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)
        self.service = get_question_service()
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
