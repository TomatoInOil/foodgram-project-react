from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

API_PATH = "api/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_PATH, include("interaction.urls", namespace="interaction")),
    path(API_PATH, include("recipes.urls", namespace="recipes")),
    path(API_PATH, include("users.urls", namespace="users")),
]

if settings.DEBUG is True:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
