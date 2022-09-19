from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.admin import AlphabeticalFilter
from users.models import Subscription, User


@admin.register(User)
class UserAdmin(UserAdmin):
    """Настройка админ-панели для модели связи рецепт-ингредиент."""

    list_display = (
        "pk",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_display_links = ("pk", "username", "email")
    list_filter = (
        AlphabeticalFilter.setup(field="username"),
        AlphabeticalFilter.setup(field="email"),
        "is_staff",
        "is_active",
    )
    staff_fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональная информация",
            {"fields": ("first_name", "last_name", "username")},
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    date_hierarchy = "date_joined"

    def get_fieldsets(self, request, obj):
        if not obj:
            return self.add_fieldsets
        if request.user.is_superuser:
            return self.fieldsets
        else:
            return self.staff_fieldsets


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели связи рецепт-ингредиент."""

    list_display = ("pk", "author", "subscriber")
