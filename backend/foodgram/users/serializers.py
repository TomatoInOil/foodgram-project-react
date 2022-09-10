from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователей."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        ]

    def get_is_subscribed(self, obj):
        """Проверяет наличие подписки пользователя на автора."""
        current_user = self.context["request"].user
        if current_user.is_authenticated:
            return obj.subs_to_him.filter(subscriber=current_user).exists()
        return False
