from typing import ClassVar
from django.db import models


class ContentRole(models.TextChoices):
    QUESTION = "question"
    CONTEXT = "context"
    OPTION = "option"
    EXPLANATION = "explanation"
    ATTACHMENT = "attachment"


class ContentType(models.TextChoices):
    TEXT = "text", "Text"
    IMAGE = "image", "Image"
    AUDIO = "audio", "Audio"
    VIDEO = "video", "Video"


class Content(models.Model):
    objects: ClassVar[models.Manager["Content"]]

    id: int
    content_type = models.CharField(
        max_length=20,
        choices=ContentType.choices,
    )

    text = models.TextField(blank=True, null=True)

    file = models.FileField(
        upload_to="content/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.content_type} - {self.id}"
