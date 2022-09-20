from rest_framework import serializers

from users.serializers import UserSerializer
from recipes.fields import Base64ImageField
from recipes.models import Ingredient, IngredientQuantity, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientQuantitySerializer(serializers.ModelSerializer):
    """Дополненный сериализатор ингредиентов информацией о количестве."""

    id = serializers.PrimaryKeyRelatedField(
        source="ingredient", queryset=Ingredient.objects.all()
    )
    name = serializers.CharField(source="ingredient.name", read_only=True)
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit", read_only=True
    )

    class Meta:
        model = IngredientQuantity
        fields = ("id", "name", "measurement_unit", "amount")


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тегов."""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")
        read_only_fields = ("name", "color", "slug")


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientQuantitySerializer(many=True)
    author = UserSerializer(default=serializers.CurrentUserDefault())
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

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

    def validate_ingredients(self, value):
        """Проверка на валидность ингредиентов."""
        seen = []
        for ingredient_quantity in value:
            amount = ingredient_quantity.get("amount")
            if amount <= 0:
                raise serializers.ValidationError(
                    "Количество ингредиента должно быть положительным числом."
                )
            ingredient = ingredient_quantity.get("ingredient")
            if ingredient in seen:
                raise serializers.ValidationError(
                    "Переданные ингредиенты содержат дубликаты."
                )
            seen.append(ingredient)
        return value

    def validate(self, data):
        """Проверяет теги на наличие и верный тип переданных данных."""
        tags = data.get("tags")
        if not tags:
            raise serializers.ValidationError({"tags": ["Обязательное поле."]})
        for tag in tags:
            if not isinstance(tag, Tag) and not isinstance(tag, int):
                raise serializers.ValidationError(
                    {"tags": [f"Ожидалось целое число, получено `{tag}`."]}
                )
            if not Tag.objects.filter(pk=tag).exists():
                raise serializers.ValidationError(
                    {"tags": [f"Тег {tag} не найден."]}
                )
        return data

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        instance = super().create(validated_data)

        self._add_tags_and_ingredients_to_recipe(instance, tags, ingredients)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        instance = super().update(instance, validated_data)

        instance.tags.clear()
        instance.ingredients.all().delete()

        self._add_tags_and_ingredients_to_recipe(instance, tags, ingredients)

        return instance

    def to_internal_value(self, data):
        data = self.validate(data)
        internal_data = super().to_internal_value(data)

        tags = data["tags"]
        tag_list = []
        for tag in tags:
            tag_list.append(Tag.objects.get(pk=tag))
        internal_data["tags"] = tags
        return internal_data

    def _add_tags_and_ingredients_to_recipe(self, instance, tags, ingredients):
        """Добавить теги и ингредиенты к рецепту."""
        for tag in tags:
            instance.tags.add(tag)
        ingedient_list = [
            IngredientQuantity(
                recipe=instance,
                ingredient=ingredient["ingredient"],
                amount=ingredient["amount"],
            )
            for ingredient in ingredients
        ]
        IngredientQuantity.objects.bulk_create(ingedient_list)


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта для вложенного использования в качестве поля."""

    class Meta(serializers.ModelSerializer):
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
