from rest_framework import serializers

from apps.auth.dto.profile import ProfileRequestDTO


class ProfileResponeSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)


class ProfileRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    def validate(self, attrs: ProfileRequestDTO) -> ProfileRequestDTO:
        request = self.context.get("request")

        if request and request.headers.get("X-Client") == "mobile":
            if not attrs.get("refresh_token"):
                raise serializers.ValidationError(
                    "refresh_token is required for mobile clients"
                )

        return attrs
