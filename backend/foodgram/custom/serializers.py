from rest_framework import serializers

from recipes.models import Recipe


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта для вложенного использования в качестве поля."""

    class Meta(serializers.ModelSerializer):
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
