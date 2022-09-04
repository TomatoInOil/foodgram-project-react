from django.conf import settings
from django.db import models

from recipes.models import Recipe

User = settings.AUTH_USER_MODEL


class RecipesList(models.Model):
    """Абстрактная модель списка рецептов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s",
        verbose_name="Кулинар",
    )
    recipes = models.ManyToManyField(
        Recipe, related_name="%(class)ss", verbose_name="Рецепты"
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        user_username = self.user.username
        return f"Список пользователя {user_username}"


class FavoriteRecipesList(RecipesList):
    """Модель списка избранных рецептов пользователя."""

    class Meta:
        verbose_name = "Список избранных рецептов"
        verbose_name_plural = "Списки избранных рецептов"


class ShoppingList(RecipesList):
    """Модель списка покупок пользователя."""

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
