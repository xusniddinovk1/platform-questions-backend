from __future__ import annotations
from typing import ClassVar
from django.db import models
from apps.questions.models.content import Content, ContentRole


class Question(models.Model):
    objects: ClassVar[models.Manager["Question"]]
    title = models.CharField(max_length=255)
    allowed_answer_types = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class QuestionContent(models.Model):
    objects: ClassVar[models.Manager["QuestionContent"]]
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="contents",
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
    )

    role = models.CharField(
        max_length=20,
        choices=ContentRole.choices,
        default=ContentRole.QUESTION,
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(
                fields=["question", "content"],
                name="unique_question_content",
            ),
        ]
        ordering: ClassVar[list[str]] = ["order", "id"]
