from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id: int
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.username or self.email or str(self.id)
