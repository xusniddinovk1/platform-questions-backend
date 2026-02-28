from __future__ import annotations

from typing import Sequence, TypedDict

from rest_framework import status as drf_status
from rest_framework.response import Response


class PaginationMeta(TypedDict):
    page: int
    limit: int
    total: int
    totalPages: int


class Meta(TypedDict, total=False):
    """
    Описание структуры meta.

    По умолчанию может быть пустым объектом {}.
    Для пагинации используется поле pagination.
    """

    pagination: PaginationMeta


class ErrorItem(TypedDict):
    status: int
    code: str
    title: str
    detail: str


class SuccessResponse(TypedDict):
    """
    Успешный ответ:

    {
        "data": <payload или null>,
        "meta": {},
        "errors": null
    }
    """

    data: object | None
    meta: Meta
    errors: None


class ErrorResponse(TypedDict):
    """
    Ошибочный ответ:

    {
        "data": null,
        "meta": {},
        "errors": [
            {
                "status": 404,
                "code": "USER_NOT_FOUND",
                "title": "User not found",
                "detail": "User with id 42 does not exist"
            }
        ]
    }
    """

    data: None
    meta: Meta
    errors: list[ErrorItem]


def build_success_response(
    data: object | None,
    *,
    meta: Meta | None = None,
    status_code: int = drf_status.HTTP_200_OK,
) -> Response:
    meta_value: Meta = {} if meta is None else meta
    body: SuccessResponse = {
        "data": data,
        "meta": meta_value,
        "errors": None,
    }
    return Response(body, status=status_code)


def build_error_response(
    *,
    status_code: int,
    code: str,
    title: str,
    detail: str,
    meta: Meta | None = None,
) -> Response:
    error_item: ErrorItem = {
        "status": status_code,
        "code": code,
        "title": title,
        "detail": detail,
    }

    meta_value: Meta = {} if meta is None else meta

    body: ErrorResponse = {
        "data": None,
        "meta": meta_value,
        "errors": [error_item],
    }
    return Response(body, status=status_code)


def build_errors_response(
    *,
    status_code: int,
    errors: Sequence[ErrorItem],
    meta: Meta | None = None,
) -> Response:
    meta_value: Meta = {} if meta is None else meta

    body: ErrorResponse = {
        "data": None,
        "meta": meta_value,
        "errors": list(errors),
    }
    return Response(body, status=status_code)
