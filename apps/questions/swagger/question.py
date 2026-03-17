from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.core.swagger.common import envelope_schema

# ===== Option schema (payload ichida) =====
option_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "text": openapi.Schema(type=openapi.TYPE_STRING, example="1989"),
        "isCorrect": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
    },
)

# ===== Payload schema =====
payload_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    description="Savol turiga qarab turli ma'lumotlar: options, imageUrls va h.k.",
    properties={
        "options": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=option_schema,
            description="Variant javoblar (text/image tipidagi savollarda bo'ladi)",
        ),
        "imageUrls": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
            description="Rasm URL'lari (image tipidagi savollarda bo'ladi)",
        ),
    },
)

# ===== Question response schema =====
question_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "title": openapi.Schema(
            type=openapi.TYPE_STRING, example="Python qachon yaratilgan?"
        ),
        "type": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="text",
            description="Savol turi: text | image",
            enum=["text", "image"],
        ),
        "answersCount": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "success": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                "failed": openapi.Schema(type=openapi.TYPE_INTEGER, example=3),
            },
        ),
        "category": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                "title": openapi.Schema(type=openapi.TYPE_STRING, example="Python"),
            },
        ),
        "isNew": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "startDeadline": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="09:00:00",
            description="HH:MM:SS formatida",
        ),
        "endDeadline": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="18:00:00",
            description="HH:MM:SS formatida",
        ),
        "payload": payload_schema,
    },
)

# ===== Pagination meta schema =====
pagination_meta_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "pagination": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "page": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                "limit": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                "total": openapi.Schema(type=openapi.TYPE_INTEGER, example=125),
                "totalPages": openapi.Schema(type=openapi.TYPE_INTEGER, example=13),
            },
        )
    },
)

# ===== Question list response schema =====
question_list_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "data": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=question_response_schema,
        ),
        "meta": pagination_meta_schema,
        "errors": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_OBJECT),
            nullable=True,
        ),
    },
)

# ===== Update request schema =====
question_create_update_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["title"],
    properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING, example="2+2 nechchi?"),
        "start_deadline": openapi.Schema(
            type=openapi.TYPE_STRING, example="09:00:00"
        ),
        "end_deadline": openapi.Schema(
            type=openapi.TYPE_STRING, example="18:00:00"
        ),
    },
)

# ===== Query params =====
question_list_query_params = [
    openapi.Parameter(
        name="page",
        in_=openapi.IN_QUERY,
        description="Sahifa raqami (default: 1)",
        type=openapi.TYPE_INTEGER,
        required=False,
        default=1,
    ),
    openapi.Parameter(
        name="limit",
        in_=openapi.IN_QUERY,
        description="Har sahifada nechta natija (default: 10, max: 100)",
        type=openapi.TYPE_INTEGER,
        required=False,
        default=10,
    ),
    openapi.Parameter(
        name="category_id",
        in_=openapi.IN_QUERY,
        description="Kategoriya ID bo'yicha filter",
        type=openapi.TYPE_INTEGER,
        required=False,
    ),
]

# ===== Swagger dekoratorlar =====
questions_list_schema = swagger_auto_schema(
    operation_summary="Questions list",
    operation_description="Savollar ro'yxatini pagination bilan qaytaradi",
    manual_parameters=question_list_query_params,
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
