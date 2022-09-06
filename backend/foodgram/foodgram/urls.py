from django.contrib import admin
from django.urls import include, path

API_PATH = "api/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_PATH, include("interaction.urls", namespace="interaction")),
    path(API_PATH, include("recipes.urls", namespace="recipes")),
    path(API_PATH, include("users.urls", namespace="users")),
]
