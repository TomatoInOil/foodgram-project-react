from rest_framework import filters

from recipes.viewsets import ListRetrieveViewSet
from recipes.serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientViewSet(ListRetrieveViewSet):
    """Представление для ингредиентов.
    Обеспечивает получения списка ингредиентов или информации об одном из них.
    """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["^name"]
