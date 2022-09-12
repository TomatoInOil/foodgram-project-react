from rest_framework import filters
from rest_framework import viewsets

from custom.viewsets import ListRetrieveViewSet
from recipes.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from recipes.models import Ingredient, Recipe, Tag
from recipes.permissions import OnlyAuthorsUpdateDelete


class IngredientViewSet(ListRetrieveViewSet):
    """Представление для ингредиентов.
    Обеспечивает получения списка ингредиентов или информации об одном из них.
    """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["^name"]
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

    def perform_destroy(self, instance):
        instance.ingredients.all().delete()
        return super().perform_destroy(instance)
