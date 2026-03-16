from rest_framework import serializers
from apps.questions.models.answer import Answer
from apps.questions.serializers.content import ContentSerializer


class AnswerSerializer(serializers.ModelSerializer):
    selected_options = ContentSerializer(many=True, read_only=True)
    user: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Answer
        fields = ("id", "question", "user", "selected_options", "created_at")
        read_only_fields = ("id", "user", "selected_options", "created_at")


class AnswerCreateSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option_ids = serializers.ListField(child=serializers.IntegerField())
