from django.urls import include, path
from rest_framework import routers

from recipes import views

app_name = "recipes"

router = routers.DefaultRouter()
router.register(r"ingredients", views.IngredientViewSet)
router.register(r"tags", views.TagViewSet)
router.register(r"recipes", views.RecipeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
