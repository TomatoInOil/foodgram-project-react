from django.utils import timezone as tz
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


def get_recipes_from_model_on_request(model, request, *args, **kwargs):
    """Находит список пользователя по запросу."""
    current_user = request.user
    return get_or_create_obj_owned_by_user(current_user, model).recipes


def get_selected_recipe_on_request(request, *args, **kwargs):
    """Находит выбранный рецепт по запросу."""
    return get_object_or_404(klass=Recipe, pk=kwargs.get("recipe_id", None))


def get_year():
    """Возвращает текущий год."""
    return tz.now().year
