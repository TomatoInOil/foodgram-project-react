from rest_framework import exceptions, serializers

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

        instance.save()
        return instance

    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)

        tag_pks = data.get("tags")
        if not tag_pks:
            raise exceptions.ValidationError({"tags": "Обязательное поле."})
        tags = []
        try:
            for tag_pk in tag_pks:
                tags.append(Tag.objects.get(pk=tag_pk))
        except Tag.DoesNotExist:
            raise exceptions.ValidationError(
                {"tags": f"Тег {tag_pk} не найден."}
            )
        except ValueError:
            tag_pk_type = type(tag_pk)
            raise exceptions.ValidationError(
                {"tags": f"Ожидалось целое число, получено {tag_pk_type}"}
            )
        internal_data["tags"] = tags

        return internal_data

    def _add_tags_and_ingredients_to_recipe(self, instance, tags, ingredients):
        """Добавить теги и ингредиенты к рецепту."""
        for tag in tags:
            instance.tags.add(tag)
        for ingredient in ingredients:
            IngredientQuantity.objects.create(
                recipe=instance,
                ingredient=ingredient["ingredient"],
                amount=ingredient["amount"],
            )


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта для вложенного использования в качестве поля."""

    class Meta(serializers.ModelSerializer):
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
