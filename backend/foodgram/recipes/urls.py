from django.urls import include, path
from rest_framework import routers

from recipes import views

router = routers.DefaultRouter()
router.register(r"ingredients", views.IngredientViewSet.as_view())


urlpatterns = [
    path("", include(router.urls)),
]
