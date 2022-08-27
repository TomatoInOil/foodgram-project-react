from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Subscription(models.Model):
    """Модель подписки на автора."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subs_to_him",
        verbose_name="Автор рецепта",
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="his_subs",
        verbose_name="Заинтересованный кулинар",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["subscriber", "author"],
                name="excluding_duplicate_subscriptions",
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("author")),
                name="author_cannot_subscribe_to_himself.",
            ),
        ]

    def __str__(self) -> str:
        subscriber_username = self.subscriber.username
        author_username = self.author.username
        return f"Подписка {subscriber_username} на {author_username}"


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
