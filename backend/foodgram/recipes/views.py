from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from custom.viewsets import ListRetrieveViewSet
from recipes.filtersets import IngredientFilter, RecipeFilter
from recipes.models import Ingredient, Recipe, Tag
from recipes.permissions import OnlyAuthorsUpdateDelete
from recipes.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)


class IngredientViewSet(ListRetrieveViewSet):
    """Представление для ингредиентов.
    Обеспечивает получения списка ингредиентов или информации об одном из них.
    """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(ListRetrieveViewSet):
    """Представление для тегов.
    Обеспечивает получение списка тегов или информации об одном из них.
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для рецептов.
    Обеспечивает CRUD для рецептов.
    """

    queryset = (
        Recipe.objects.all()
        .prefetch_related("ingredients", "tags")
        .select_related("author")
    )
    serializer_class = RecipeSerializer
    permission_classes = [OnlyAuthorsUpdateDelete]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
