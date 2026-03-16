from __future__ import annotations

from rest_framework import serializers


class MeUpdateSerializer(serializers.Serializer):
    """
    Сериализатор для частичного обновления данных текущего пользователя.
    """

    username = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=False,
        help_text="Новый username пользователя",
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=False,
        help_text="Новый email пользователя",
    )
    first_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=False,
        help_text="Новое имя пользователя",
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=False,
        help_text="Новая фамилия пользователя",
    )
