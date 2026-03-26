from rest_framework import serializers

from apps.auth.dto.google_oauth import GoogleCallbackRequestDTO


class GoogleCallbackSerializer(serializers.Serializer[GoogleCallbackRequestDTO]):
    code = serializers.CharField(
        required=True,
        help_text="Authorization code from Google redirect",
    )
    state = serializers.CharField(
        required=True,
        help_text="State token for CSRF verification",
    )

    def validate(self, attrs: dict[str, str]) -> GoogleCallbackRequestDTO:
        return GoogleCallbackRequestDTO(
            code=attrs["code"],
            state=attrs["state"],
        )
