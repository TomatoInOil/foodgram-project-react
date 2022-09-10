from django.contrib.auth import get_user_model
from rest_framework import serializers

from custom.serializers import ShortRecipeSerializer

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


class UserWithRecipesSerializer(UserSerializer):
    """Сериализатор пользователя с добавлением им написанных рецептов."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["recipes", "recipes_count"]

    def get_recipes(self, obj):
        "Получить рецепты пользователя, написанные им."
        recipes_limit = int(
            self.context.get("request").query_params.get("recipes_limit")
        )
        if recipes_limit:
            return ShortRecipeSerializer(
                instance=obj.recipes.all()[:recipes_limit], many=True
            ).data
        return ShortRecipeSerializer(
            instance=obj.recipes.all(), many=True
        ).data

    def get_recipes_count(self, obj):
        """Получить количество показанных рецептов."""
        return obj.recipes.all().count()
