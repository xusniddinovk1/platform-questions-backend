from rest_framework import serializers


class RefreshSuccessResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()
