from recipes.serializers import RecipeSerializer


class RecipeSerializer(RecipeSerializer):
    """Сериализатор для рецепта, добавленного в избранное."""

    class Meta(RecipeSerializer.Meta):
        fields = ("id", "name", "image", "cooking_time")
