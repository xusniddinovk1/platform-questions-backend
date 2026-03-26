from django.db import models

from apps.user.models import User


class AuthProvider(models.TextChoices):
    EMAIL = "email", "Email"
    GOOGLE = "google", "Google"


class SocialAccount(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="social_accounts"
    )
    provider = models.CharField(max_length=20, choices=AuthProvider.choices)
    provider_id = models.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = ("provider", "provider_id")

    def __str__(self) -> str:
        return f"{self.provider}:{self.provider_id} -> {self.user}"
