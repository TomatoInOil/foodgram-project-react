from django.http import HttpResponse
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from interaction.models import FavoriteRecipesList, ShoppingList
from custom.serializers import ShortRecipeSerializer
from services.interaction_sevices import (
    add_selected_recipe_to_recipes_list,
    create_lines_of_text_document_from_shopping_list,
    delete_selected_recipe_from_recipes_list,
    get_or_create_obj_owned_by_current_user,
    get_selected_recipe_on_request,
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
        selected_recipe = get_selected_recipe_on_request(
            request, *args, **kwargs
        )
        error_response = add_selected_recipe_to_recipes_list(
            selected_recipe, request, self.model, self.name_of_list
        )
        if error_response:
            return error_response
        return Response(
            data=ShortRecipeSerializer(instance=selected_recipe).data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        """Удаляет связь рецепта и списка избранных рецептов пользователя."""
        selected_recipe = get_selected_recipe_on_request(
            request, *args, **kwargs
        )
        error_response = delete_selected_recipe_from_recipes_list(
            selected_recipe, request, self.model, self.name_of_list
        )
        if error_response:
            return error_response
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteRecipesListView(RecipesListView):
    """Представление для списка избранных рецептов пользователя."""

    name_of_list = "избранного"
    model = FavoriteRecipesList


class ShoppingListView(RecipesListView):
    """Представление для списка покупок пользователя."""

    name_of_list = "покупок"
    model = ShoppingList


class DownloadShoppingListView(views.APIView):
    """Представление для скачивания списка покупок."""

    model = ShoppingList
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Отдаёт файл со списком покупок пользователя."""
        shopping_list = get_or_create_obj_owned_by_current_user(
            request, self.model
        )
        lines = create_lines_of_text_document_from_shopping_list(
            shopping_list, request
        )
        response_content = "\n".join(lines)
        response = HttpResponse(
            response_content, content_type="text/plain;charset=UTF-8"
        )
        response[
            "Content-Disposition"
        ] = "attachment; filename=shopping_list.txt"
        return response
