from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.core.swagger.common import envelope_schema

content_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "content_type": openapi.Schema(type=openapi.TYPE_STRING, example="text"),
        "text": openapi.Schema(type=openapi.TYPE_STRING, example="Savol matni"),
        "file": openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
        "created_at": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
    },
    required=["content_type"],
)


question_content_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "role": openapi.Schema(type=openapi.TYPE_STRING),
        "order": openapi.Schema(type=openapi.TYPE_INTEGER),
        "is_correct": openapi.Schema(type=openapi.TYPE_BOOLEAN),
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


question_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "title": openapi.Schema(type=openapi.TYPE_STRING),
        "allowed_answer_types": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
        ),
        "created_at": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
        "answersCount": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "success": openapi.Schema(type=openapi.TYPE_INTEGER),
                "failed": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        "category": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "title": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        "isNew": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "startDeadline": openapi.Schema(type=openapi.TYPE_STRING, format="time"),
        "endDeadline": openapi.Schema(type=openapi.TYPE_STRING, format="time"),
        "contents": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=question_content_response_schema,
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


question_list_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "data": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=question_response_schema,
        ),
        "meta": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "pagination": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "page": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "limit": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "total": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "totalPages": openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                )
            },
        ),
        "errors": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_OBJECT),
            nullable=True,
        ),
    },
)


questions_list_schema = swagger_auto_schema(
    operation_summary="Questions list",
    responses={200: envelope_schema(question_list_response_schema)},
    tags=["Questions"],
)


get_question_by_id_schema = swagger_auto_schema(
    operation_summary="Get question by id",
    operation_description="Bitta questionni pk orqali qaytaradi",
    responses={200: envelope_schema(question_response_schema)},
    tags=["Questions"],
)


update_question_partial_schema = swagger_auto_schema(
    operation_summary="Update question partially",
    operation_description="Savolni qisman yangilash",
    request_body=question_create_update_request_schema,
    responses={200: envelope_schema(question_response_schema)},
    tags=["Questions"],
)
