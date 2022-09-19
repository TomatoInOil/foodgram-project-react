from django.contrib import admin
from django.db.models.aggregates import Count

from core.admin import AlphabeticalFilter
from recipes.models import Ingredient, IngredientQuantity, Recipe, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели ингредиентов."""

    list_display = ("pk", "name", "measurement_unit")
    list_display_links = ("pk", "name")
    list_filter = (AlphabeticalFilter.setup(field="name"),)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели тегов."""

    list_display = ("pk", "name", "color", "slug")
    list_display_links = ("pk", "name")


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели рецептов."""

    list_display = (
        "pk",
        "name",
        "author__username",
        "tags",
        "in_favorites",
        "pub_date",
    )
    list_display_links = ("pk", "name")
    list_filter = (
        AlphabeticalFilter.setup(field="name"),
        AlphabeticalFilter.setup(field="author__username"),
        "tags",
    )
    date_hierarchy = "pub_date"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(in_favorites=Count("favoriterecipeslists"))

    def in_favorites(self, obj):
        """Количество пользователей добавивших рецепт в избранное."""
        return obj.in_favorites


@admin.register(IngredientQuantity)
class IngredientQuantityAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели связи рецепт-ингредиент."""

    list_display = ("pk", "recipe", "ingredient", "amount")
