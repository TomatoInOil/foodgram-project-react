from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


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
                check=~models.Q(subscriber=models.F("author")),
                name="author_cannot_subscribe_to_himself.",
            ),
        ]

    def __str__(self) -> str:
        subscriber_username = self.subscriber.username
        author_username = self.author.username
        return f"Подписка {subscriber_username} на {author_username}"
