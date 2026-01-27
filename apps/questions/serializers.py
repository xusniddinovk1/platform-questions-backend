from __future__ import annotations

from typing import Any, cast

from django.db import transaction
from rest_framework import serializers

from .models import Answer, Content, ContentRole, ContentType, Question, QuestionContent


class ContentSerializer(serializers.ModelSerializer[Content]):
    class Meta:
        model = Content
        fields = ("id", "content_type", "text", "file", "created_at")
        read_only_fields = ("id", "created_at")

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        content_type = attrs.get(
            "content_type", getattr(self.instance, "content_type", None)
        )
        text = attrs.get("text", getattr(self.instance, "text", None))
        file = attrs.get("file", getattr(self.instance, "file", None))

        if content_type == ContentType.TEXT:
            if not text:
                raise serializers.ValidationError({"text": "TEXT uchun `text` majburiy."})
        else:
            if not file:
                raise serializers.ValidationError(
                    {"file": f"{content_type} uchun `file` majburiy."}
                )

        return attrs


class QuestionContentSerializer(serializers.ModelSerializer[QuestionContent]):
    content = ContentSerializer()

    class Meta:
        model = QuestionContent
        fields = ("id", "role", "order", "content")
        read_only_fields = ("id",)


class QuestionSerializer(serializers.ModelSerializer[Question]):
    contents = QuestionContentSerializer(many=True, read_only=True)
    answers_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "title",
            "allowed_answer_types",
            "created_at",
            "contents",
            "answers_count",
        )
        read_only_fields = ("id", "created_at", "contents", "answers_count")


class QuestionCreateUpdateSerializer(serializers.ModelSerializer[Question]):
    contents_payload = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Question
        fields = ("id", "title", "allowed_answer_types", "created_at", "contents_payload")
        read_only_fields = ("id", "created_at")

    @transaction.atomic
    def create(self, validated_data: dict[str, Any]) -> Question:
        payload = validated_data.pop("contents_payload", [])
        question: Question = super().create(validated_data)
        self._upsert_contents(question, payload, replace=True)
        return question

    @transaction.atomic
    def update(self, instance: Question, validated_data: dict[str, Any]) -> Question:
        payload = validated_data.pop("contents_payload", None)
        question: Question = super().update(instance, validated_data)
        if payload is not None:
            self._upsert_contents(question, payload, replace=True)
        return question

    def _upsert_contents(
        self,
        question: Question,
        payload: list[dict[str, Any]],
        *,
        replace: bool,
    ) -> None:
        if replace:
            QuestionContent.objects.filter(question=question).delete()

        for item in payload:
            role = item.get("role", ContentRole.QUESTION)
            order = item.get("order", 0)
            content_data = item.get("content")

            if not isinstance(content_data, dict):
                raise serializers.ValidationError(
                    {
                        "contents_payload": (
                            "Har bir item ichida `content` dict bo'lishi kerak."
                        )
                    }
                )

            content_ser = ContentSerializer(data=content_data)
            content_ser.is_valid(raise_exception=True)
            content_obj = cast(Content, content_ser.save())

            QuestionContent.objects.create(
                question=question,
                content=content_obj,
                role=role,
                order=order,
            )


class AnswerSerializer(serializers.ModelSerializer[Answer]):
    content = ContentSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

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
        content_obj = cast(Content, content_ser.save())

        return Answer.objects.create(
            question=question,
            user_id=user_id,
            content=content_obj,
        )
