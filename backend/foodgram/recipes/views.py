from rest_framework import filters
from rest_framework import viewsets

from recipes.viewsets import ListRetrieveViewSet
from recipes.serializers import IngredientSerializer, RecipeSerializer
from recipes.models import Ingredient, Recipe


class IngredientsViewSet(ListRetrieveViewSet):
    """Представление для ингредиентов.
    Обеспечивает получения списка ингредиентов или информации об одном из них.
    """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["^name"]


class RecipesViewSet(viewsets.ModelViewSet):
    """Представление для рецептов.
    Обеспечивает CRUD для рецептов.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
