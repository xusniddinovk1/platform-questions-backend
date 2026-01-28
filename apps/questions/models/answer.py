from typing import ClassVar
from django.db import models
from apps.questions.models.mics import Content
from apps.questions.models.question import Question
from django.conf import settings


class Answer(models.Model):
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
