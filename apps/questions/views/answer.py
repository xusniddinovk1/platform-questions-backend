from rest_framework import permissions, serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.questions.repositories.answer import AnswerRepository
from apps.questions.repositories.question import QuestionRepository
from apps.questions.serializers.answer import AnswerSerializer
from apps.questions.services.answer import (
    AnswerAlreadyExists,
    AnswerService,
    AnswerTypeNotAllowed,
    CreateAnswerCommand,
)

answer_service = AnswerService(
    question_repo=QuestionRepository(),
    answer_repo=AnswerRepository(),
)


class AnswerCreateAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request: Request) -> Response:
        question_raw = request.data.get("question")
        if question_raw is None:
            raise ValidationError({"question": "Majburiy."})

        user_id = request.user.id
        if user_id is None:
            raise ValidationError({"user": "User topilmadi."})

        cmd = CreateAnswerCommand(
            question_id=int(question_raw),
            user_id=int(user_id),
            content=request.data.get("content") or {},
        )

        try:
            answer = answer_service.create_answer(cmd)
        except AnswerAlreadyExists:
            raise ValidationError("Siz bu savolga allaqachon javob bergansiz.")
        except AnswerTypeNotAllowed as e:
            msg = (
                f"Ruxsat etilgan turlar: {e.allowed}. "
                f"Siz yubordingiz: {e.sent}"
            )
            raise ValidationError({"content": msg})
        except serializers.ValidationError as e:
            raise ValidationError(e.detail) from e

        return Response(
            AnswerSerializer(answer).data,
            status=status.HTTP_201_CREATED,
        )
class AnswerViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,  # type: ignore[type-arg]
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Answer]:
        return answers_queryset_for_request(self.request)

    def get_serializer_class(self) -> type[Serializer]:  # type: ignore[type-arg]
        if self.action == "create":
            return AnswerCreateSerializer
        return AnswerSerializer

    def create(
        self,
        request: Request,
        *args: object,
        **kwargs: object,
    ) -> Response:
        answer = create_answer(request)
        out = AnswerSerializer(answer, context={"request": request})
        return Response(out.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="mine")
    def mine(self, request: Request) -> Response:
        qs = self.get_queryset()

        page = self.paginate_queryset(qs)
        if page is not None:
            ser = AnswerSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(ser.data)

        ser = AnswerSerializer(qs, many=True, context={"request": request})
        return Response(ser.data)