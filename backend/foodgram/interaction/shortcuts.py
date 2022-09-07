from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe


def get_or_create_obj_owned_by_user(user, model):
    """Возвращает или создаёт объект принадлежащий пользователю."""
    return model.objects.get_or_create(user=user)[0]


def create_error_response(msg):
    """Возвращает объект Response с ошибкой 400."""
    return Response(
        data={"error": msg},
        status=status.HTTP_400_BAD_REQUEST,
    )


def get_selected_recipe_and_recipes_from_model_on_request(
    model, request, *args, **kwargs
):
    """По запросу находит выбранный рецепт и список пользователя из запроса."""
    current_user = request.user
    recipes_from_list = get_or_create_obj_owned_by_user(
        current_user, model
    ).recipes

    selected_recipe = get_object_or_404(
        klass=Recipe, pk=kwargs.get("recipe_id", None)
    )
    return recipes_from_list, selected_recipe
