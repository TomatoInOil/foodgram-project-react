from rest_framework import filters
from rest_framework import viewsets

from custom.viewsets import ListRetrieveViewSet
from recipes.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from recipes.models import Ingredient, Recipe, Tag


class IngredientViewSet(ListRetrieveViewSet):
    """Представление для ингредиентов.
    Обеспечивает получения списка ингредиентов или информации об одном из них.
    """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["^name"]


class TagViewSet(ListRetrieveViewSet):
    """Представление для тегов.
    Обеспечивает получение списка тегов или информации об одном из них.
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для рецептов.
    Обеспечивает CRUD для рецептов.
    """

    queryset = Recipe.objects.all().prefetch_related("ingredients", "tags")
    serializer_class = RecipeSerializer
