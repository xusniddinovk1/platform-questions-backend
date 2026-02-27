from rest_framework import serializers
from apps.questions.models.question import Question
from apps.questions.serializers.questionContent import QuestionContentSerializer


class QuestionSerializer(serializers.ModelSerializer):
    contents = QuestionContentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "title", "allowed_answer_types", "contents", "created_at")
        read_only_fields = ("id", "contents", "created_at")
