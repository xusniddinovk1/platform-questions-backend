from rest_framework import serializers
from apps.questions.models.mics import Content, ContentType


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("id", "content_type", "text", "file", "created_at")
        read_only_fields = ("id", "created_at")

    def validate(self, attrs):
        ct = attrs.get("content_type")
        text = attrs.get("text")
        file = attrs.get("file")

        if ct == ContentType.TEXT:
            if not text:
                raise serializers.ValidationError({"text": "TEXT uchun `text` majburiy."})
        else:
            if not file:
                raise serializers.ValidationError({"file": f"{ct} uchun `file` majburiy."})

        return attrs
