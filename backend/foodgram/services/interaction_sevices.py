from pathlib import Path
from typing import Union

from django.conf import settings
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
    recipe_id = kwargs.get("recipe_id", None)
    return get_object_or_404(klass=Recipe, pk=recipe_id)


def add_selected_recipe_to_recipes_list(
    selected_recipe, request, model, name_of_list
) -> Union[None, Response]:
    """Добавляет выбранный рецепт в список избранных рецептов пользователя.
    Если рецепт уже добавлен в список, возвращает response с ошибкой.
    """
    recipes_from_list = get_or_create_obj_owned_by_current_user(
        request, model
    ).recipes
    if selected_recipe in recipes_from_list.all():
        return create_response_with_error_message(
            msg=f"Рецепт уже добавлен в список {name_of_list}."
        )
    recipes_from_list.add(selected_recipe)
    return None


def delete_selected_recipe_from_recipes_list(
    selected_recipe, request, model, name_of_list
) -> Union[None, Response]:
    """Удаляет выбранный рецепт из списка избранных рецептов пользователя.
    Если рецепт уже удалён из списка, возвращает response с ошибкой.
    """
    recipes_from_list = get_or_create_obj_owned_by_current_user(
        request, model
    ).recipes
    if selected_recipe not in recipes_from_list.all():
        return create_response_with_error_message(
            msg=f"Рецепта нет в списке {name_of_list}."
        )
    recipes_from_list.remove(selected_recipe)
    return None


def get_filepath_related_to_shopping_list(shopping_list):
    """Возвращает путь до файла списка покупок."""
    shopping_lists_path = Path.joinpath(settings.MEDIA_ROOT, "shopping_lists/")
    if not settings.MEDIA_ROOT.exists():
        Path.mkdir(settings.MEDIA_ROOT)
    if not shopping_lists_path.exists():
        Path.mkdir(shopping_lists_path)
    return Path.joinpath(
        shopping_lists_path,
        f"shopping_list_{shopping_list.id}.txt",
    )


def write_text_of_shopping_list_to_file(filepath, shopping_list, request):
    """Записывает текст списка покупок в указанный файл."""
    with open(filepath, "w", encoding="utf-8") as file:
        lines = _create_lines_of_text_document_from_shopping_list(
            shopping_list, request
        )
        file.writelines(lines)
        file.close()


def _create_lines_of_text_document_from_shopping_list(shopping_list, request):
    """Формирует из списка покупок строки текстового документа."""
    lines = []
    for recipe in shopping_list.recipes.all():
        lines.append(f"- - - {recipe.name} - - - \n")
        recipe_ingredients = recipe.ingredients.select_related(
            "ingredient"
        ).all()
        for ingredient in recipe_ingredients:
            name = ingredient.ingredient.name
            amount = str(ingredient.amount)
            measurement_unit = ingredient.ingredient.measurement_unit
            lines.append(
                " ".join(["[ ]", name, amount, measurement_unit, "\n"])
            )
    host = request.get_host()
    year = tz.now().year
    lines.append(f"\n {host} {year}")
    return lines