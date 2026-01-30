from rest_framework import serializers

from apps.auth.dto.logout import LogoutRequestDto


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    def validate(self, attrs: LogoutRequestDto) -> LogoutRequestDto:
        request = self.context.get("request")

        if request and request.headers.get("X-Client") == "mobile":
            if not attrs.get("refresh_token"):
                raise serializers.ValidationError(
                    "refresh_token is required for mobile clients"
                )

        return attrs
