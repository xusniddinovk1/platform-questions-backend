from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.questions.serializers.question import QuestionSerializer

content_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "content_type": openapi.Schema(type=openapi.TYPE_STRING, example="text"),
        "text": openapi.Schema(
            type=openapi.TYPE_STRING, example="Savol matni shu yerda..."
        ),
        "file": openapi.Schema(
            type=openapi.TYPE_STRING, format="uri", example="https://example.com/file.png"
        ),
        "created_at": openapi.Schema(
            type=openapi.TYPE_STRING, format="date-time", example="2026-02-24T12:00:00Z"
        ),
    },
    required=["content_type"],
)

question_content_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "role": openapi.Schema(type=openapi.TYPE_STRING, example="question"),
        "order": openapi.Schema(type=openapi.TYPE_INTEGER, example=0),
        "content": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                "content_type": openapi.Schema(type=openapi.TYPE_STRING, example="text"),
                "text": openapi.Schema(
                    type=openapi.TYPE_STRING, example="Savol matni..."
                ),
                "file": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="uri",
                    example="https://example.com/file.png",
                ),
                "created_at": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date-time",
                    example="2026-02-24T12:00:00Z",
                ),
            },
        ),
    },
)

question_create_update_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["title"],
    properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING, example="2+2 nechchi?"),
        "allowed_answer_types": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            example=["text", "number"],
        ),
        "contents_payload": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description=(
                "Content'larni yaratib question'ga bog'laydi (replace=True). "
                "Har bir element content bilan bog'lanadi."
            ),
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "role": openapi.Schema(type=openapi.TYPE_STRING, example="question"),
                    "order": openapi.Schema(type=openapi.TYPE_INTEGER, example=0),
                    "content": content_schema,
                },
                required=["content"],
            ),
            example=[
                {
                    "role": "question",
                    "order": 0,
                    "content": {"content_type": "text", "text": "2+2 nechchi?"},
                }
            ],
        ),
    },
)

question_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
        "title": openapi.Schema(type=openapi.TYPE_STRING, example="2+2 nechchi?"),
        "allowed_answer_types": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            example=["text", "number"],
        ),
        "created_at": openapi.Schema(
            type=openapi.TYPE_STRING, format="date-time", example="2026-02-24T12:00:00Z"
        ),
        "answers_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=0),
        "contents": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=question_content_response_schema,
        ),
    },
)

question_list_response_schema = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=question_response_schema,
)
questions_list_schema = swagger_auto_schema(
    operation_summary="Questions list",
    operation_description="Barcha savollar ro'yxatini qaytaradi",
    responses={
        200: question_list_response_schema,
    },
    tags=["Questions"],
)

get_question_by_id_schema = swagger_auto_schema(
    operation_summary="Get question by id",
    operation_description="Bitta questionni pk orqali qaytaradi",
    responses={
        200: question_response_schema,
        404: "Question not found",
    },
    tags=["Questions"],
)

update_question_partial_schema = swagger_auto_schema(
    operation_summary="Update question partially",
    operation_description="Savolni qisman yangilash",
    request_body=QuestionSerializer,
    responses={
        200: question_response_schema,
        400: "Invalid data",
        404: "Question not found",
    },
    tags=["Questions"],
)
