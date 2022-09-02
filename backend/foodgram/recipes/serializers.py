from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ["id", "name", "measurement_unit"]


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тегов."""

    class Meta:
        model = Tag
        fields = ["id", "name", "color", "slug"]


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецептов."""

    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "tags",
            # "author",
            # "ingredients",
            # "is_favorited",
            # "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        ]
