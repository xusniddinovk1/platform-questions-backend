from typing import Any

from rest_framework import serializers
from apps.questions.models.content import Content, ContentType


class ContentSerializer(serializers.ModelSerializer):
    """
    Serializer for Content model.
    Validates required fields depending on content type.
    """

    class Meta:
        model = Content
        fields = ("id", "content_type", "text", "file", "created_at")
        read_only_fields = ("id", "created_at")

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        ct = attrs.get("content_type")
        text = attrs.get("text")
        file = attrs.get("file")

        if ct == ContentType.TEXT:
            if not text:
                raise serializers.ValidationError({"text": "TEXT uchun `text` majburiy."})
        else:
            if not file:
                raise serializers.ValidationError(
                    {"file": f"{ct} uchun `file` majburiy."}
                )

        return attrs
