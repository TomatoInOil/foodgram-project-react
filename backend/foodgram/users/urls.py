from django.urls import include, path
from rest_framework import routers

from users import views

app_name = "users"

router = routers.DefaultRouter()
router.register(r"users", views.UsersViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
