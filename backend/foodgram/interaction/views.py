from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from rest_framework import status, views
from rest_framework.response import Response

from interaction.models import FavoriteRecipesList, ShoppingList
from interaction.serializers import RecipeSerializer
from interaction.shortcuts import (
    create_error_response,
    get_or_create_obj_owned_by_user,
    get_recipes_from_model_on_request,
    get_selected_recipe_on_request,
    get_year,
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
        recipes_from_list = get_recipes_from_model_on_request(
            self.model, request, *args, **kwargs
        )
        selected_recipe = get_selected_recipe_on_request(
            request, *args, **kwargs
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
        recipes_from_list = get_recipes_from_model_on_request(
            self.model, request, *args, **kwargs
        )
        selected_recipe = get_selected_recipe_on_request(
            request, *args, **kwargs
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


class DownloadShoppingListView(views.APIView):
    """Представление для скачивания списка покупок."""

    model = ShoppingList

    def get(self, request, *args, **kwargs):
        """Отдаёт файл со списком покупок пользователя."""
        current_user = request.user
        shopping_list = get_or_create_obj_owned_by_user(
            current_user, self.model
        )

        shopping_lists_path = Path.joinpath(
            settings.MEDIA_ROOT, "shopping_lists/"
        )
        if not settings.MEDIA_ROOT.exists():
            Path.mkdir(settings.MEDIA_ROOT)
        if not shopping_lists_path.exists():
            Path.mkdir(shopping_lists_path)
        filepath = Path.joinpath(
            shopping_lists_path,
            f"shopping_list_{shopping_list.id}.txt",
        )

        with open(filepath, "w", encoding="utf-8") as file:
            rows = []

            for recipe in shopping_list.recipes.all():
                rows.append(f"- - - {recipe.name} - - - \n")
                recipe_ingredients = recipe.ingredients.all()
                for ingredient in recipe_ingredients:
                    name = ingredient.ingredient.name
                    amount = str(ingredient.amount)
                    measurement_unit = ingredient.ingredient.measurement_unit
                    rows.append(
                        " ".join(["[ ]", name, amount, measurement_unit, "\n"])
                    )

            host = request.get_host()
            year = get_year()
            rows.append(f"{host} {year}")

            file.writelines(rows)
            file.close()

        with open(filepath, "r", encoding="utf-8") as file:
            return HttpResponse(file, status=status.HTTP_200_OK)
