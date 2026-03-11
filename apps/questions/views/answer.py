from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.questions.container import get_answer_service
from apps.questions.serializers.answer import (
    AnswerCreateSerializer,
    AnswerSerializer,
)
from apps.questions.services.answer import (
    CreateAnswerCommand,
    AnswerAlreadyExists,
)
from apps.questions.swagger.answer import create_answer_schema
from apps.core.responses import build_success_response, build_error_response
from apps.core.logger import LoggerType, get_logger_service


class AnswerCreateAPIView(APIView):
    log: LoggerType
    permission_classes = (permissions.IsAuthenticated,)

    def __init__(self, **kwargs: dict[str, object]) -> None:
        super().__init__(**kwargs)

        self.log = get_logger_service(__name__)

    @create_answer_schema
    def post(self, request: Request) -> Response:
        serializer = AnswerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = request.user.id
        if user_id is None:
            self.log.error("User ID is None when trying to create an answer")
            raise ValueError("User ID cannot be None")

        cmd = CreateAnswerCommand(
            question_id=serializer.validated_data["question_id"],
            user_id=user_id,
            selected_option_ids=serializer.validated_data["selected_option_ids"],
        )

        service = get_answer_service()

        try:
            answer = service.create_answer(cmd)
            self.log.info(f"Answer created successfully for user_id={user_id}")
            return build_success_response(
                data=AnswerSerializer(answer).data,
                status_code=status.HTTP_201_CREATED
            )

        except AnswerAlreadyExists:
            self.log.warning(f"User {user_id} attempted to create a duplicate answer")
            return build_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                code="ANSWER_ALREADY_EXISTS",
                title="Answer already exists",
                detail="Siz allaqachon javob bergansiz."
            )
