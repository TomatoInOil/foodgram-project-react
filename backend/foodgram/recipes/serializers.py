from rest_framework import serializers

from recipes.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ["id", "name", "measurement_unit"]


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецептов."""

    class Meta:
        model = Recipe
        fields = [
            "id",
            # "tags",
            # "author",
            # "ingredients",
            # "is_favorited",
            # "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        ]
