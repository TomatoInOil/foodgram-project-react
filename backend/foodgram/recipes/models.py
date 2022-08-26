from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(max_length=200, verbose_name="Название")
    measurement_unit = models.CharField(
        max_length=16, verbose_name="Единицы измерения"
    )


class Recipe(models.Model):
    """Модель рецептов."""

    name = models.CharField(max_length=200, verbose_name="Название")
    tags = models.ManyToManyField("Tags", verbose_name="Теги")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientQuantity",
        through_fields=("recipe", "ingredient"),
        verbose_name="Ингредиенты",
    )
    image = models.ImageField(verbose_name="Картинка")
    text = models.TextField(verbose_name="Текстовое описание")
    cooking_time = models.IntegerField(verbose_name="Время приготовления")
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)


class IngredientQuantity(models.Model):
    """Связь рецепта и ингредиента с указанием количества."""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент"
    )
    number = models.FloatField(verbose_name="Количество")
