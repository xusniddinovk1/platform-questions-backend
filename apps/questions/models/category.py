from django.db import models
from typing import ClassVar


class Category(models.Model):
    objects: ClassVar[models.Manager["Category"]]
    id: int

    title = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
