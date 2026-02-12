from rest_framework import serializers
from apps.questions.models.question import QuestionContent, Question
from apps.questions.serializers.mics import ContentSerializer


class QuestionContentSerializer(serializers.ModelSerializer):
    content = ContentSerializer(read_only=True)

    class Meta:
        model = QuestionContent
        fields = ("id", "role", "order", "content")
        read_only_fields = fields


class QuestionSerializer(serializers.ModelSerializer):
    contents = QuestionContentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "title", "allowed_answer_types", "contents", "created_at")
        read_only_fields = ("id", "contents", "created_at")
