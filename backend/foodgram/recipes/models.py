from colorfield.fields import ColorField
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(max_length=200, verbose_name="Название")
    measurement_unit = models.CharField(
        max_length=16, verbose_name="Единицы измерения"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(max_length=200, verbose_name="Название")
    color = ColorField(default="#FF0000", format="hex", verbose_name="Цвет")
    slug = models.SlugField(max_length=200)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self) -> str:
        return self.name


def recipe_directory_path(instance, filename):
    """Формирует путь для сохранения картинки рецепта."""
    return "user_{0}/{1}".format(instance.author_id, filename)


class Recipe(models.Model):
    """Модель рецептов."""

    name = models.CharField(max_length=200, verbose_name="Название")
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="recipes",
    )
    image = models.ImageField(
        verbose_name="Картинка", upload_to=recipe_directory_path
    )
    text = models.TextField(verbose_name="Текстовое описание")
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата публикации"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-pub_date"]

    def __str__(self) -> str:
        return self.name


class IngredientQuantity(models.Model):
    """Связь рецепта и ингредиента с указанием количества."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Ингредиент",
    )
    amount = models.FloatField(verbose_name="Количество")

    class Meta:
        verbose_name = "Связь рецепт-ингредиент"
        verbose_name_plural = "Связи рецепт-ингредиент"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="excluding_duplicate_ingredients",
            ),
            models.CheckConstraint(
                check=models.Q(amount__gt=0),
                name="amount_of_ingredient_must_be_positive_number",
            ),
        ]

    def __str__(self) -> str:
        recipe_id = self.recipe.id
        ingredient_id = self.ingredient.id
        return f"В рецепт {recipe_id} входит ингредиент {ingredient_id}"
