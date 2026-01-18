from typing import ClassVar
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.permissions import BasePermission
from rest_framework.serializers import BaseSerializer

from .serializers import QuestionSerializer, AnswerCreateSerializer
from rest_framework.exceptions import ValidationError
from .models import Question, Answer


class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer
    permission_classes: ClassVar[list[type[BasePermission]]] = [
        permissions.AllowAny
    ]


class QuestionDetailVIew(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes: ClassVar[list[type[BasePermission]]] = [
        permissions.AllowAny
    ]


class AnswerCreateView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerCreateSerializer
    permission_classes: ClassVar[list[type[BasePermission]]] = [
        permissions.IsAuthenticated
    ]

    def perform_create(self, serializer: BaseSerializer) -> None:
        question = serializer.validated_data['question']

        if question.deadline <= timezone.now():
            raise ValidationError({'detail': 'Closed'})

        if Answer.objects.filter(user=self.request.user, question=question).exists():
            raise ValidationError({'detail': 'Answer already exists'})

        serializer.save(user=self.request.user)
