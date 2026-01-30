from drf_yasg import openapi

content_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "content_type": openapi.Schema(
            type=openapi.TYPE_STRING, example="text"
        ),
        "text": openapi.Schema(
            type=openapi.TYPE_STRING, example="Savol matni shu yerda..."
        ),
        "file": openapi.Schema(
            type=openapi.TYPE_STRING, format="uri", example=None
        ),
        "created_at": openapi.Schema(
            type=openapi.TYPE_STRING, format="date-time"
        ),
    },
    required=["content_type"],
)


question_content_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(
            type=openapi.TYPE_INTEGER, example=1
        ),
        "role": openapi.Schema(
            type=openapi.TYPE_STRING, example="question"
        ),
        "order": openapi.Schema(type=openapi.TYPE_INTEGER, example=0),
        "content": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, example=10
                ),
                "content_type": openapi.Schema(
                    type=openapi.TYPE_STRING, example="text"
                ),
                "text": openapi.Schema(
                    type=openapi.TYPE_STRING, example="Savol matni..."
                ),
                "file": openapi.Schema(
                    type=openapi.TYPE_STRING, format="uri", example=None
                ),
                "created_at": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date-time"
                ),
            },
        ),
    },
)

# CREATE/UPDATE request body
question_create_update_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["title"],
    properties={
        "title": openapi.Schema(
            type=openapi.TYPE_STRING, example="2+2 nechchi?"
        ),
        "allowed_answer_types": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            example=["text", "number"],
        ),
        "contents_payload": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description="Content'larni yaratib question'ga bog'laydi (replace=True)",
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "role": openapi.Schema(
                        type=openapi.TYPE_STRING, example="question"
                    ),
                    "order": openapi.Schema(
                        type=openapi.TYPE_INTEGER, example=0)
                    ,
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

# Response: QuestionSerializer ga mos
question_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(
            type=openapi.TYPE_INTEGER, example=5
        ),
        "title": openapi.Schema(
            type=openapi.TYPE_STRING, example="2+2 nechchi?"
        ),
        "allowed_answer_types": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            example=["text", "number"],
        ),
        "created_at": openapi.Schema(
            type=openapi.TYPE_STRING, format="date-time"
        ),
        "answers_count": openapi.Schema(
            type=openapi.TYPE_INTEGER, example=0
        ),
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
