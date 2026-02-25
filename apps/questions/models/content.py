from typing import ClassVar

from django.db import models


class ContentRole(models.TextChoices):
    QUESTION = "question", "Question"
    CONTEXT = "context", "Context"
    EXPLANATION = "explanation", "Explanation"
    ATTACHMENT = "attachment", "Attachment"


class ContentType(models.TextChoices):
    TEXT = "text", "Text"
    IMAGE = "image", "Image"
    AUDIO = "audio", "Audio"
    VIDEO = "video", "Video"


class Content(models.Model):
    objects: ClassVar[models.Manager["Content"]]

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
