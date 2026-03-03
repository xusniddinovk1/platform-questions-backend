from typing import ClassVar
from django.db import models
from apps.questions.models.content import Content
from apps.questions.models.question import Question


class QuestionOption(models.Model):
    objects: ClassVar[models.Manager["QuestionOption"]]

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
    )

    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
    )

    is_correct = models.BooleanField(default=False)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering: ClassVar[list[str]] = ["order", "id"]
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["question", "content"],
                name="unique_option_per_question",
            ),
        ]

    def __str__(self) -> str:
        return f"Option for {self.question.pk}"
