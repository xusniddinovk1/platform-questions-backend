from rest_framework import serializers
from apps.questions.models.answer import Answer
from apps.questions.serializers.content import ContentSerializer



class AnswerSerializer(serializers.ModelSerializer):
    content = ContentSerializer(read_only=True)
    user: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Answer
        fields = ("id", "question", "user", "content", "created_at")
        read_only_fields = ("id", "user", "content", "created_at")

class AnswerCreateSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    content = serializers.JSONField()
