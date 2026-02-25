from __future__ import annotations
from typing import ClassVar
from django.conf import settings
from django.db import models
from apps.questions.models.content import Content


class Answer(models.Model):
    objects: ClassVar[models.Manager["Answer"]]

    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="answers",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["question", "user"],
                name="unique_user_answer_per_question",
            ),
        ]
