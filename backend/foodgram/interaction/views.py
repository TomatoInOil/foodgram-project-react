from rest_framework import status, views
from rest_framework.response import Response

from interaction.models import FavoriteRecipesList, ShoppingList
from interaction.serializers import RecipeSerializer
from interaction.shortcuts import (
    create_error_response,
    get_selected_recipe_and_recipes_from_model_on_request,
)


class RecipesListView(views.APIView):
    """Абстрактное представление для списков пользователя.
    Обеспечивает добавление рецепта в список и удаление из него.
    При наследовании нужно указать:
      name_of_list = "избранного", если список избранного
      model = модель списка рецептов.
    """

    name_of_list = ...
    model = ...

    def post(self, request, *args, **kwargs):
        """Добавляет рецепт в список избранных рецептов пользователя."""
        (
            recipes_from_list,
            selected_recipe,
        ) = get_selected_recipe_and_recipes_from_model_on_request(
            self.model, request, *args, **kwargs
        )

        if selected_recipe in recipes_from_list.all():
            return create_error_response(
                msg=f"Рецепт уже добавлен в список {self.name_of_list}."
            )

        recipes_from_list.add(selected_recipe)
        return Response(
            data=RecipeSerializer(instance=selected_recipe).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        """Удаляет связь рецепта и списка избранных рецептов пользователя."""
        (
            recipes_from_list,
            selected_recipe,
        ) = get_selected_recipe_and_recipes_from_model_on_request(
            self.model, request, *args, **kwargs
        )

        if selected_recipe not in recipes_from_list.all():
            return create_error_response(
                msg=f"Рецепта нет в списке {self.name_of_list}."
            )

        recipes_from_list.remove(selected_recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteRecipesListView(RecipesListView):
    """Представление для списка избранных рецептов пользователя."""

    name_of_list = "избранного"
    model = FavoriteRecipesList


class ShoppingListView(RecipesListView):
    """Представление для списка покупок пользователя."""

    name_of_list = "покупок"
    model = ShoppingList
