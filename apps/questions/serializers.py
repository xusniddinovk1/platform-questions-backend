from django.contrib.auth import get_user_model
from rest_framework import serializers
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
        fields = ['id', 'user', 'answer']


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'deadline', 'created_at', 'updated_at', 'answers']
