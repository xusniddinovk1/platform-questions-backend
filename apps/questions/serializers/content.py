
from rest_framework import serializers
from apps.questions.models.content import Content, ContentType


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("id", "content_type", "text", "file", "created_at")
        read_only_fields = ("id", "created_at")

    def validate(self, attrs: dict) -> dict:
        ct = attrs.get("content_type")
        text = attrs.get("text")
        file = attrs.get("file")

        if ct == ContentType.TEXT and not text:
            raise serializers.ValidationError(
                {"text": "TEXT uchun text majburiy"}
            )

        if ct != ContentType.TEXT and not file:
            raise serializers.ValidationError({"file": "File majburiy"})

        return attrs
