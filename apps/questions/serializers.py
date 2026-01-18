from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Question, Answer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'user', 'answer', 'status', 'score', 'created_at']
        read_only_fields = ['user', 'created_at']


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer']

        def validate(self, attrs):
            question = attrs.get['question']
            if question.deadline <= timezone.now():
                raise ValidationError({'detail': 'Closed'})
            return attrs


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'deadline', 'created_at', 'updated_at', 'answers']
