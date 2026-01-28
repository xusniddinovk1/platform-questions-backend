from typing import ClassVar, cast, Any
from django.db import transaction
from rest_framework import serializers
from apps.questions.models.question import Question
from apps.questions.models.answer import Answer
from apps.questions.serializers.mics import ContentSerializer


class AnswerSerializer(serializers.ModelSerializer[Answer]):
    content = ContentSerializer(read_only=True)
    user: ClassVar[object] = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ("id", "question", "user", "content", "created_at")
        read_only_fields = ("id", "user", "content", "created_at")


class AnswerCreateSerializer(serializers.Serializer[Answer]):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    content = ContentSerializer()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        question: Question = attrs["question"]
        user_id = cast(int, self.context["request"].user.id)

        allowed = list(question.allowed_answer_types or [])
        content_type = attrs["content"]["content_type"]

        if allowed and content_type not in allowed:
            msg = (
                "Bu savol uchun ruxsat etilgan turlar: "
                f"{allowed}. Siz yubordingiz: {content_type}"
            )
            raise serializers.ValidationError({"content": msg})

        if Answer.objects.filter(question=question, user_id=user_id).exists():
            raise serializers.ValidationError(
                "Siz bu savolga allaqachon javob bergansiz."
            )

        return attrs

    @transaction.atomic
    def create(self, validated_data: dict[str, Any]) -> Answer:
        question: Question = validated_data["question"]
        user_id = cast(int, self.context["request"].user.id)

        content_data = validated_data["content"]
        content_ser = ContentSerializer(data=content_data)
        content_ser.is_valid(raise_exception=True)
        content_obj = content_ser.save()

        return Answer.objects.create(
            question=question,
            user_id=user_id,
            content=content_obj,
        )
