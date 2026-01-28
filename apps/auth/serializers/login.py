from rest_framework import serializers

from apps.auth.dto import LoginEmailRequestDTO
from apps.user.models import User


class LoginSerializer(serializers.Serializer[User]):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: LoginEmailRequestDTO) -> LoginEmailRequestDTO:
        email = attrs["email"]
        password = attrs["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Неверные учетные данные")

        if not user.check_password(password):
            raise serializers.ValidationError("Неверные учетные данные")

        return LoginEmailRequestDTO(email=email, password=password)
