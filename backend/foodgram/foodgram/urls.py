from django.contrib import admin
from django.urls import path, include

API_PATH = "api/"

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_PATH, include("users.urls", namespace="users")),
]
