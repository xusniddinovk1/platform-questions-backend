from __future__ import annotations
from typing import Any
from rest_framework import serializers
from apps.questions.models.mics import Content, ContentType
from apps.questions.models.question import QuestionContent


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
