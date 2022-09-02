from django.urls import include, path
from rest_framework import routers

from recipes import views

app_name = "recipes"

router = routers.DefaultRouter()
router.register(r"ingredients", views.IngredientsViewSet)
router.register(r"recipes", views.RecipesViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
