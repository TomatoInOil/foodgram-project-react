from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from interaction.models import FavoriteRecipesList


def get_favorites_list(user):
    """Возвращает список избранного пользователя."""
    return FavoriteRecipesList.objects.get_or_create(user=user)[0]


def create_error_response(msg):
    """Возвращает объект Response с ошибкой."""
    return Response(
        data={"error": msg},
        status=status.HTTP_400_BAD_REQUEST,
    )


def get_selected_recipe_and_favorite_recipes(request, *args, **kwargs):
    """По запросу находит выбранный рецепт и список избранного."""
    current_user = request.user
    favorite_recipes = get_favorites_list(user=current_user).recipes

    selected_recipe = get_object_or_404(
        klass=Recipe, pk=kwargs.get("recipe_id", None)
    )
    return favorite_recipes, selected_recipe
