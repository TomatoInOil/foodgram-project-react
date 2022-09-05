from django.contrib import admin

from recipes.models import Ingredient, Recipe, Tag, IngredientQuantity


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели ингредиентов."""

    list_display = ("pk", "name", "measurement_unit")
    list_display_links = ("pk", "name")


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
        "author",
        "image",
        "text",
        "cooking_time",
        "pub_date",
    )
    list_display_links = ("pk", "name")
    date_hierarchy = "pub_date"


@admin.register(IngredientQuantity)
class IngredientQuantityAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели связи рецепт-ингредиент."""

    list_display = ("pk", "recipe", "ingredient", "amount")
