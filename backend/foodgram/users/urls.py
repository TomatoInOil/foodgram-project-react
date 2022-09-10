from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView

from users import views

app_name = "users"

urlpatterns = [
    path(
        "users/subscriptions/",
        views.MySubscriptionsView.as_view(),
        name="mysubs",
    ),
    path(
        "users/<int:author_id>/subscribe/",
        views.SubscribeView.as_view(),
        name="subscribe",
    ),
    path("", include("djoser.urls")),
    path("auth/token/login/", TokenCreateView.as_view(), name="login"),
    path("auth/token/logout/", TokenDestroyView.as_view(), name="logout"),
]
