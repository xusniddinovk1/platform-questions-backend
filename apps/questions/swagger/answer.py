from drf_yasg.utils import swagger_auto_schema
from apps.questions.serializers.answer import AnswerCreateSerializer, AnswerSerializer

create_answer_schema = swagger_auto_schema(
    operation_summary="Create answer",
    operation_description="Savolga javob yaratadi",
    request_body=AnswerCreateSerializer,
    responses={
        201: AnswerSerializer,
        400: "Validation error",
    },
    tags=["Answers"],
)
