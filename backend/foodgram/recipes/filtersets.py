from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    """Фильтр рецептов по тегам, спискам рецептов, авторам."""

    tags = filters.CharFilter(field_name="tags__slug", lookup_expr="iexact")
    is_favorited = filters.BooleanFilter(
        field_name="favoriterecipeslists__user",
        method="filter_is_in_recipes_list",
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name="shoppinglists__user", method="filter_is_in_recipes_list"
    )

    def filter_is_in_recipes_list(self, queryset, name, value):
        current_user = self.request.user
        lookup = "__".join([name, "exact"])
        if value:
            return queryset.filter(**{lookup: current_user})
        return queryset.exclude(**{lookup: current_user})

    class Meta:
        model = Recipe
        fields = ["author"]
