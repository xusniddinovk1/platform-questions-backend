from __future__ import annotations
from typing import ClassVar
from django.db import models
from django.conf import settings
from apps.questions.models.option import QuestionOption
from apps.questions.models.question import Question


class Answer(models.Model):
    objects: ClassVar[models.Manager["Answer"]]

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    selected_option = models.ForeignKey(
        QuestionOption,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="answers",
    )

    text_answer = models.TextField(
        null=True,
        blank=True,
    )

    is_correct = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["question", "user"],
                name="unique_user_answer_per_question",
            ),
        ]

    def __str__(self) -> str:
        return f"Answer by {self.user_id} for {self.question_id}"