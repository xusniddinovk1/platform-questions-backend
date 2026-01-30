from rest_framework import serializers

from apps.user.models.user_model import User


class RegisterEmailSerializer(serializers.ModelSerializer[User]):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")
