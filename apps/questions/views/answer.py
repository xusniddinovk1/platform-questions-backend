from __future__ import annotations
from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from apps.questions.common.pagination import Pagination
from apps.questions.models.answer import Answer
from apps.questions.serializers.answer import AnswerCreateSerializer, AnswerSerializer
from apps.questions.services.answer import answers_queryset_for_request, create_answer


PAGINATION_PARAMS = [
    openapi.Parameter("page", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    openapi.Parameter("page_size", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
]


class AnswerListCreateAPI(
    mixins.ListModelMixin,
    GenericAPIView,
):
    permission_classes: tuple[type[BasePermission], ...] = (IsAuthenticated,)
    pagination_class = Pagination

    def get_queryset(self) -> QuerySet[Answer]:
        return answers_queryset_for_request(self.request)

    def get_serializer_class(self) -> type[Serializer]:
        return AnswerCreateSerializer if self.request.method == "POST" else AnswerSerializer

    @swagger_auto_schema(
        operation_summary="Answerlar ro'yxati",
        manual_parameters=PAGINATION_PARAMS,
        responses={200: AnswerSerializer(many=True)},
        tags=["Answers"],
    )
    def get(self, request: Request, *args: object, **kwargs: object) -> Response:
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Answer yaratish",
        request_body=AnswerCreateSerializer,
        responses={201: AnswerSerializer()},
        tags=["Answers"],
    )
    def post(self, request: Request, *args: object, **kwargs: object) -> Response:
        answer = create_answer(request)
        out = AnswerSerializer(answer, context={"request": request})
        return Response(out.data, status=status.HTTP_201_CREATED)


class AnswerRetrieveAPI(
    mixins.RetrieveModelMixin,
    GenericAPIView,
):
    permission_classes: tuple[type[BasePermission], ...] = (IsAuthenticated,)
    pagination_class = None
    serializer_class = AnswerSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self) -> QuerySet[Answer]:
        return answers_queryset_for_request(self.request)

    @swagger_auto_schema(
        operation_summary="Bitta answer olish",
        responses={200: AnswerSerializer()},
        tags=["Answers"],
    )
    def get(self, request: Request, pk: int, *args: object, **kwargs: object) -> Response:
        return self.retrieve(request, *args, **kwargs)


class MyAnswersAPI(
    mixins.ListModelMixin,
    GenericAPIView,
):
    permission_classes: tuple[type[BasePermission], ...] = (IsAuthenticated,)
    pagination_class = Pagination
    serializer_class = AnswerSerializer

    def get_queryset(self) -> QuerySet[Answer]:
        return answers_queryset_for_request(self.request)

    @swagger_auto_schema(
        operation_summary="Mening answerlarim",
        manual_parameters=PAGINATION_PARAMS,
        responses={200: AnswerSerializer(many=True)},
        tags=["Answers"],
    )
    def get(self, request: Request, *args: object, **kwargs: object) -> Response:
        return self.list(request, *args, **kwargs)
