from rest_framework import serializers

from apps.auth.dto import RegisterDTO
from apps.user.models.user_model import User


class RegisterSerializer(serializers.ModelSerializer[User]):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email", "phone")

    def create(self, validated_data: RegisterDTO) -> User:
        return User.objects.create_user(**validated_data)
