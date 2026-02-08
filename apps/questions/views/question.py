from __future__ import annotations
from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from apps.auth.permissions import IsAdminOrReadOnly
from apps.questions.common.pagination import Pagination
from apps.questions.models.question import Question
from apps.questions.serializers.question import (
    QuestionCreateUpdateSerializer,
    QuestionSerializer,
)
from apps.questions.services.question import build_questions_queryset
from apps.questions.swagger.question import (
    question_create_update_request_schema,
    question_list_response_schema,
    question_response_schema,
)

PAGINATION_PARAMS = [
    openapi.Parameter("page", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    openapi.Parameter("page_size", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
]


class QuestionListCreateAPI(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView,
):
    permission_classes: tuple[type[BasePermission], ...] = (IsAdminOrReadOnly,)
    pagination_class = Pagination

    def get_queryset(self) -> QuerySet[Question]:
        return build_questions_queryset()

    def get_serializer_class(self) -> type[Serializer]:
        return (
            QuestionCreateUpdateSerializer
            if self.request.method == "POST"
            else QuestionSerializer
        )

    @swagger_auto_schema(
        operation_summary="Questionlar ro'yxati",
        manual_parameters=PAGINATION_PARAMS,
        responses={200: openapi.Response(
            description="OK",
            schema=question_list_response_schema
        )},
        tags=["Questions"],
    )
    def get(self,
            request: Request,
            *args: object,
            **kwargs: object
            ) -> Response:
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Question yaratish",
        request_body=question_create_update_request_schema,
        responses={201: openapi.Response(
            description="Created",
            schema=question_response_schema
        )},
        tags=["Questions"],
    )
    def post(self,
             request: Request,
             *args: object,
             **kwargs: object
             ) -> Response:
        return self.create(request, *args, **kwargs)


class QuestionRetrieveUpdateAPI(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericAPIView,
):
    permission_classes: tuple[type[BasePermission], ...] = (IsAdminOrReadOnly,)
    pagination_class = None
    lookup_url_kwarg = "pk"

    def get_queryset(self) -> QuerySet[Question]:
        return build_questions_queryset()

    def get_serializer_class(self) -> type[Serializer]:
        return (
            QuestionCreateUpdateSerializer
            if self.request.method in {"PUT", "PATCH"}
            else QuestionSerializer
        )

    @swagger_auto_schema(
        operation_summary="Bitta question olish",
        responses={200: openapi.Response(
            description="OK",
            schema=question_response_schema
        )},
        tags=["Questions"],
    )
    def get(self,
            request: Request,
            pk: int,
            *args: object,
            **kwargs: object
            ) -> Response:
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Question yangilash (PUT)",
        request_body=question_create_update_request_schema,
        responses={200: openapi.Response(
            description="OK",
            schema=question_response_schema
        )},
        tags=["Questions"],
    )
    def put(self,
            request: Request,
            pk: int,
            *args: object,
            **kwargs: object
            ) -> Response:
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Question qisman yangilash (PATCH)",
        request_body=question_create_update_request_schema,
        responses={200: openapi.Response(
            description="OK",
            schema=question_response_schema
        )},
        tags=["Questions"],
    )
    def patch(self,
              request: Request,
              pk: int,
              *args: object,
              **kwargs: object
              ) -> Response:
        return self.partial_update(request, *args, **kwargs)
