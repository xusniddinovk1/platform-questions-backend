from rest_framework import serializers
from apps.questions.models.question import QuestionContent
from apps.questions.serializers.mics import ContentSerializer


class QuestionContentSerializer(serializers.ModelSerializer):
    content = ContentSerializer(read_only=True)

    class Meta:
        model = QuestionContent
        fields = ("id", "role", "order", "content")
        read_only_fields = fields
