from __future__ import annotations

from typing import Any

from rest_framework import status as drf_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.core.responses import ErrorItem, build_errors_response


def _build_error_items_from_data(
    data: Any,
    *,
    status_code: int,
    default_code: str,
    default_title: str,
) -> list[ErrorItem]:
    errors: list[ErrorItem] = []

    def _flatten(prefix: str, value: Any) -> None:
        if isinstance(value, list):
            message = "; ".join(str(item) for item in value)
            detail = f"{prefix}: {message}" if prefix else message
            errors.append(
                {
                    "status": status_code,
                    "code": default_code,
                    "title": default_title,
                    "detail": detail,
                }
            )
        elif isinstance(value, dict):
            for key, nested in value.items():
                nested_prefix = "" if key == "non_field_errors" else key
                _flatten(nested_prefix, nested)
        else:
            errors.append(
                {
                    "status": status_code,
                    "code": default_code,
                    "title": default_title,
                    "detail": str(value),
                }
            )

    _flatten("", data)
    return errors


def custom_exception_handler(exc: Exception, context: dict[str, object]) -> Response | None:
    """
    Глобальный обработчик исключений, который приводит ответы к общей
    схеме {data, meta, errors} для DRF-ошибок.
    """
    response = exception_handler(exc, context)

    # Если DRF не знает, как обработать исключение — оставляем как есть.
    if response is None:
        return None

    # Если ответ уже в нужной обёртке, не трогаем его.
    if isinstance(response.data, dict) and {
        "data",
        "meta",
        "errors",
    }.issubset(response.data.keys()):
        return response

    status_code = response.status_code

    # Специальная обработка ValidationError (в том числе serializer.is_valid)
    if isinstance(exc, ValidationError):
        errors = _build_error_items_from_data(
            response.data,
            status_code=status_code,
            default_code="VALIDATION_ERROR",
            default_title="Validation error",
        )

        return build_errors_response(
            status_code=status_code,
            errors=errors,
            meta={},
        )

    # Для остальных стандартных ошибок DRF (AuthenticationFailed, NotFound и т.п.)
    # приводим к общей схеме, но без детальной типизации по коду.
    errors = _build_error_items_from_data(
        response.data,
        status_code=status_code,
        default_code="ERROR",
        default_title="Error",
    )

    return build_errors_response(
        status_code=status_code,
        errors=errors,
        meta={},
    )

