from django.urls import path

from interaction import views

app_name = "interaction"

urlpatterns = [
    path(
        "recipes/<int:recipe_id>/favorite/",
        views.FavoriteRecipesListView.as_view(),
        name="favorite",
    ),
    path(
        "recipes/<int:recipe_id>/shopping_cart/",
        views.ShoppingListView.as_view(),
        name="favorite",
    ),
]
