from typing import Union

from django.shortcuts import get_object_or_404
from django.utils import timezone as tz
from rest_framework.response import Response

from recipes.models import Recipe
from services.services import create_response_with_error_message


def get_or_create_obj_owned_by_current_user(request, model):
    """Возвращает объект принадлежащий пользователю."""
    return model.objects.get_or_create(user=request.user)[0]


def get_selected_recipe_on_request(request, *args, **kwargs):
    """Находит выбранный рецепт по запросу."""
    recipe_id = kwargs.get("recipe_id")
    return get_object_or_404(klass=Recipe, pk=recipe_id)


def add_selected_recipe_to_recipes_list(
    selected_recipe, request, model, name_of_list
) -> Union[None, Response]:
    """Добавляет выбранный рецепт в список избранных рецептов пользователя.
    Если рецепт уже добавлен в список, возвращает response с ошибкой.
    """
    recipes_list = get_or_create_obj_owned_by_current_user(request, model)
    if recipes_list.recipes.filter(pk=selected_recipe.id).exists():
        return create_response_with_error_message(
            msg=f"Рецепт уже добавлен в список {name_of_list}."
        )
    recipes_list.recipes.add(selected_recipe)
    return None


def delete_selected_recipe_from_recipes_list(
    selected_recipe, request, model, name_of_list
) -> Union[None, Response]:
    """Удаляет выбранный рецепт из списка избранных рецептов пользователя.
    Если рецепт уже удалён из списка, возвращает response с ошибкой.
    """
    recipes_list = get_or_create_obj_owned_by_current_user(request, model)
    if not recipes_list.recipes.filter(pk=selected_recipe.id).exists():
        return create_response_with_error_message(
            msg=f"Рецепта нет в списке {name_of_list}."
        )
    recipes_list.recipes.remove(selected_recipe)
    return None


def create_lines_of_text_document_from_shopping_list(shopping_list, request):
    """Формирует из списка покупок строки текстового документа."""
    ingredients = shopping_list.recipes.values_list(
        "ingredients__ingredient__name",
        "ingredients__amount",
        "ingredients__ingredient__measurement_unit",
    )
    lines = []
    for ingredient in ingredients:
        lines.append(
            " ".join([ingredient[0], str(ingredient[1]), ingredient[2]])
        )
    host = request.get_host()
    year = tz.now().year
    lines.append(f"{host} {year}")
    return lines
