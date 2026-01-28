from typing import Any
from django.db import transaction
from rest_framework import serializers
from apps.questions.models.mics import ContentRole
from apps.questions.models.question import Question, QuestionContent
from apps.questions.serializers.mics import (
    QuestionContentSerializer,
    ContentSerializer
)


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
            content_obj = content_ser.save()

            QuestionContent.objects.create(
                question=question,
                content=content_obj,
                role=role,
                order=order,
            )
