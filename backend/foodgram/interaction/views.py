from rest_framework import status, views
from rest_framework.response import Response

from interaction.serializers import FavoriteRecipeSerializer
from interaction.shortcuts import (
    create_error_response,
    get_selected_recipe_and_favorite_recipes,
)


class FavoriteRecipesListView(views.APIView):
    """Представление для списка избранных рецептов пользователя."""

    def post(self, request, *args, **kwargs):
        """Добавляет рецепт в список избранных рецептов пользователя."""
        (
            favorite_recipes,
            selected_recipe,
        ) = get_selected_recipe_and_favorite_recipes(request, *args, **kwargs)

        if selected_recipe in favorite_recipes.all():
            return create_error_response(
                msg="Рецепт уже добавлен в избранное."
            )

        favorite_recipes.add(selected_recipe)
        return Response(
            data=FavoriteRecipeSerializer(instance=selected_recipe).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        """Удаляет связь рецепта и списка избранных рецептов пользователя."""
        (
            favorite_recipes,
            selected_recipe,
        ) = get_selected_recipe_and_favorite_recipes(request, *args, **kwargs)

        if selected_recipe not in favorite_recipes.all():
            return create_error_response(msg="Рецепта нет в избранном.")

        favorite_recipes.remove(selected_recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)
