from django.contrib import admin

from core.admin import AlphabeticalFilter
from users.models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели связи рецепт-ингредиент."""

    list_display = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_display_links = ("pk", "username", "email")
    list_filter = (
        AlphabeticalFilter.setup(field="username"),
        AlphabeticalFilter.setup(field="email"),
        "is_staff",
        "is_active",
    )
    date_hierarchy = "date_joined"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели связи рецепт-ингредиент."""

    list_display = ("pk", "author", "subscriber")
