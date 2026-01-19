from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.auth.dto import LoginInput, LoginOutput
from apps.user.models.user_model import User


class LoginSerializer(serializers.Serializer[User]):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: LoginInput) -> LoginOutput:
        username = attrs["username"]
        password = attrs["password"]

        user = authenticate(username=username, password=password)
        if not user or not isinstance(user, User):
            raise serializers.ValidationError("Неверные учетные данные")

        return {"user": user}
