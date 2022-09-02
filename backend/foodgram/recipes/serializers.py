from rest_framework import serializers

from recipes.models import Ingredient, IngredientQuantity, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientQuantitySerializer(serializers.ModelSerializer):
    """Дополненный сериализатор ингредиентов информацией о количестве."""

    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientQuantity
        fields = ("id", "name", "measurement_unit", "amount")


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тегов."""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецептов."""

    tags = TagSerializer(many=True)
    ingredients = IngredientQuantitySerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            # "author",
            "ingredients",
            # "is_favorited",
            # "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
