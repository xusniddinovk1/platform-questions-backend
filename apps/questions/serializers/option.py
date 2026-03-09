from rest_framework import serializers
from apps.questions.models.question import QuestionContent


class OptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="content.id")
    text = serializers.CharField(source="content.text")
    isCorrect = serializers.BooleanField(source="is_correct")

    class Meta:
        model = QuestionContent
        fields = ("id", "text", "isCorrect")
