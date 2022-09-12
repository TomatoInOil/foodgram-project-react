from rest_framework import serializers

from recipes.models import Ingredient, IngredientQuantity, Recipe, Tag
from users.serializers import UserSerializer


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
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        """Есть ли рецепт в списке избранного текущего пользователя."""
        current_user = self.context["request"].user
        if current_user.is_authenticated:
            return obj.favoriterecipeslists.filter(user=current_user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        """Есть ли рецепт в списке покупок текущего пользователя."""
        current_user = self.context["request"].user
        if current_user.is_authenticated:
            return obj.shoppinglists.filter(user=current_user).exists()
        return False


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта для вложенного использования в качестве поля."""

    class Meta(serializers.ModelSerializer):
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
