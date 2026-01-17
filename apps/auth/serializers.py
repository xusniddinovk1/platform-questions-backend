# from django.contrib.auth import authenticate, get_user_model
# from rest_framework import serializers

# # from apps.user.models import User
# from .dto import LoginDTO, RegisterDTO

# User = get_user_model()


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, attrs: LoginDTO) -> LoginDTO | None:
#         user = authenticate(
#             username=attrs.get("username"), password=attrs.get("password")
#         )
#         if not user:
#             raise serializers.ValidationError("Неверные учетные данные")
#         attrs["user"] = user
#         return attrs


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ("username", "password", "email", "phone")

#     def create(self, validated_data: RegisterDTO) -> User:
#         user = User.objects.create_user(**validated_data)
#         return user

# apps/auth/serializers.py


from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.user.models import User

from .dto import LoginInput, LoginOutput, RegisterDTO


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


class RegisterSerializer(serializers.ModelSerializer[User]):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email", "phone")

    def create(self, validated_data: RegisterDTO) -> User:
        return User.objects.create_user(**validated_data)
