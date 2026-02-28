from drf_yasg import openapi


def envelope_schema(data_schema: openapi.Schema | None = None) -> openapi.Schema:
    """
    Общая схема-обёртка для всех JSON-ответов:

    {
        "data": ...,
        "meta": {
            "pagination": {
                "page": 1,
                "limit": 10,
                "total": 100,
                "totalPages": 10
            }
        },
        "errors": null | [
            {
                "status": 404,
                "code": "USER_NOT_FOUND",
                "title": "User not found",
                "detail": "User with id 42 does not exist"
            }
        ]
    }
    """

    pagination_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "page": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            "limit": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
            "total": openapi.Schema(type=openapi.TYPE_INTEGER, example=100),
            "totalPages": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
        },
        required=["page", "limit", "total", "totalPages"],
    )

    meta_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "pagination": pagination_schema,
        },
    )

    error_item_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "status": openapi.Schema(type=openapi.TYPE_INTEGER, example=404),
            "code": openapi.Schema(
                type=openapi.TYPE_STRING,
                example="USER_NOT_FOUND",
            ),
            "title": openapi.Schema(
                type=openapi.TYPE_STRING,
                example="User not found",
            ),
            "detail": openapi.Schema(
                type=openapi.TYPE_STRING,
                example="User with id 42 does not exist",
            ),
        },
        required=["status", "code", "title", "detail"],
    )

    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "data": data_schema
            or openapi.Schema(type=openapi.TYPE_OBJECT, description="Payload"),
            "meta": meta_schema,
            "errors": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=error_item_schema,
                nullable=True,
            ),
        },
        required=["data", "meta", "errors"],
    )
