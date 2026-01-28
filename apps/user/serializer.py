from rest_framework import serializers

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name")
