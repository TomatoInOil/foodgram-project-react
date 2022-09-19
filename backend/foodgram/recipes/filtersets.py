from django_filters import rest_framework as filters

from recipes.models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    """Фильтр рецептов по тегам, спискам рецептов, авторам."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
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


class IngredientFilter(filters.FilterSet):
    """Фильтр ингредиентов по имени."""

    name = filters.CharFilter(field_name="name", lookup_expr="istartswith")
