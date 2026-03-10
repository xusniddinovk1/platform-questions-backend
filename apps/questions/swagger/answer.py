from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.core.swagger.common import envelope_schema

# ===== Answer response schema =====
answer_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "question": openapi.Schema(type=openapi.TYPE_INTEGER),
        "user": openapi.Schema(type=openapi.TYPE_INTEGER),
        "created_at": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
        "content": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "content_type": openapi.Schema(type=openapi.TYPE_STRING),
                "text": openapi.Schema(type=openapi.TYPE_STRING),
                "file": openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                "created_at": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date-time"
                ),
            },
        ),
    },
)

# ===== Create answer swagger =====
create_answer_schema = swagger_auto_schema(
    operation_summary="Create answer",
    operation_description="Savolga javob yaratadi",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "question_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "content": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "content_type": openapi.Schema(type=openapi.TYPE_STRING),
                    "text": openapi.Schema(type=openapi.TYPE_STRING),
                    "file": openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                },
                required=["content_type"],
            ),
        },
        required=["question_id", "content"],
    ),
    responses={
        201: envelope_schema(answer_response_schema),
        400: envelope_schema(
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING),
                },
            )
        ),
    },
    tags=["Answers"],
)
