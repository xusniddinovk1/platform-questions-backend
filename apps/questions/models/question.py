from __future__ import annotations
from typing import ClassVar
from django.db import models
from typing import TYPE_CHECKING
from apps.questions.models.content import Content, ContentRole

if TYPE_CHECKING:
    from .answer import Answer
    from django.db.models.manager import Manager as RelatedManager



class Category(models.Model):
    objects: ClassVar[models.Manager["Category"]]

    title = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    objects: ClassVar[models.Manager["Question"]]
    if TYPE_CHECKING:
        answers: 'RelatedManager["Answer"]'

    title = models.CharField(max_length=255)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    allowed_answer_types = models.JSONField(
        default=list,
        blank=True
    )

    start_deadline = models.TimeField(
        blank=True,
        null=True
    )

    end_deadline = models.TimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return self.title

class QuestionContent(models.Model):
    objects: ClassVar[models.Manager["QuestionContent"]]

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="contents"
    )

    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ContentRole.choices,
        default=ContentRole.QUESTION
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_correct = models.BooleanField(
        default=False
    )

    class Meta:
        ordering: ClassVar[list[str]] = ["order"]
