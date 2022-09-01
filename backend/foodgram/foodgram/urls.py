from django.contrib import admin
from django.urls import include, path

API_PATH = "api/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_PATH, include("recipes.url", namespace="recipes")),
]
