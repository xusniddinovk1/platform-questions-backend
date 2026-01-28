from django.db import models

from .user_model import User


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student",
    )

    university = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255)
    course = models.PositiveSmallIntegerField()
    admission_year = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Student: {self.user}"
