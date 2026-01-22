from django.conf import settings
from django.contrib.postgres.fields import ArrayField
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


class Question(models.Model):
    title = models.CharField(max_length=255)

    allowed_answer_types = ArrayField(
        models.CharField(
            max_length=20,
            choices=ContentType.choices,
        ),
        default=list,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class QuestionContent(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="contents",
    )
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    role = models.CharField(
        max_length=20,
        choices=ContentRole.choices,
        default=ContentRole.QUESTION,
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["question", "content"],
                name="unique_question_content",
            ),
        ]
        ordering = ["order", "id"]


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["question", "user"],
                name="unique_user_answer_per_question",
            ),
        ]
