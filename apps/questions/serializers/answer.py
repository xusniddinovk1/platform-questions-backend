from typing import ClassVar, Any, cast

from django.db import transaction, IntegrityError
from rest_framework import serializers
from apps.questions.models.answer import Answer
from apps.questions.models.question import Question
from apps.questions.serializers.mics import ContentSerializer


class AnswerSerializer(serializers.ModelSerializer):
    content = ContentSerializer(read_only=True)
    user: ClassVar[object] = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ("id", "question", "user", "content", "created_at")
        read_only_fields = ("id", "user", "content", "created_at")


class AnswerCreateSerializer(serializers.Serializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    content = ContentSerializer()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        question: Question = attrs["question"]
        user_id = cast(int, self.context["request"].user.id)

        allowed = list(question.allowed_answer_types or [])
        content_type = attrs["content"]["content_type"]

        if allowed and content_type not in allowed:
            raise serializers.ValidationError(
                {"content": f"Ruxsat etilgan turlar: {allowed}. Siz yubordingiz: {content_type}"}
            )

        if Answer.objects.filter(question=question, user_id=user_id).exists():
            raise serializers.ValidationError("Siz bu savolga allaqachon javob bergansiz.")

        return attrs

    @transaction.atomic
    def create(self, validated_data: dict[str, Any]) -> Answer:
        question: Question = validated_data["question"]
        user = self.context["request"].user

        content_ser = ContentSerializer(data=validated_data["content"])
        content_ser.is_valid(raise_exception=True)
        content_obj = content_ser.save()

        try:
            return Answer.objects.create(
                question=question,
                user=user,
                content=content_obj,
            )
        except IntegrityError:
            raise serializers.ValidationError("Siz bu savolga allaqachon javob bergansiz.")
