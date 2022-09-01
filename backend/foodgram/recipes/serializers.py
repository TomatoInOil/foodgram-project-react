from rest_framework import serializers

from recipes.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ["name", "measurement_unit"]
