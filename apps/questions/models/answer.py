from __future__ import annotations
from typing import ClassVar
from django.db import models
from apps.questions.models.content import Content
from apps.questions.models.question import Question
from django.conf import settings


class Answer(models.Model):
    objects: ClassVar[models.Manager["Answer"]]
    id: int
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    selected_options = models.ManyToManyField(Content, blank=True)

    is_correct = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
