from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from typing import ClassVar, Any

from .models import Question, Answer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields: ClassVar[list[str]] = ["id", "username"]


class AnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields: ClassVar[list[str]] = ["id",
                                       "user",
                                       "answer",
                                       "status",
                                       "score",
                                       "created_at"]
        read_only_fields: ClassVar[list[str]] = ["user", "created_at"]


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields: ClassVar[list[str]] = ["id", "question", "answer"]

        def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
            question = attrs.get("question")
            if question and question.deadline <= timezone.now():
                raise serializers.ValidationError("Deadline closed")
            return attrs


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields: ClassVar[list[str]] = [
            "id",
            "title",
            "description",
            "deadline",
            "created_at",
            "updated_at",
            "answers",
        ]
