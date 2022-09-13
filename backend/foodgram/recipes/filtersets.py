from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    """Фильтр рецептов по тегам с помощью slug."""

    tags = filters.CharFilter(field_name="tags__slug", lookup_expr="iexact")

    class Meta:
        model = Recipe
        fields = ["tags"]
