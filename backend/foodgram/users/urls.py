from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from users import views

app_name = "users"

router = routers.DefaultRouter()
router.register(r"users", views.UsersViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/login/", TokenCreateView.as_view(), name="login"),
    path("auth/token/logout/", TokenDestroyView.as_view(), name="logout"),
    # path("api/users/set_password/"),
]
