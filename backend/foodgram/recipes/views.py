from recipes.viewsets import ListRetrieveViewSet
from recipes.serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientViewSet(ListRetrieveViewSet):
    """Представление для ингредиентов.
    Обеспечивает получения списка ингредиентов или информации об одном из них.
    """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
