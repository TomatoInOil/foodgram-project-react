from django.contrib import admin

from users.models import User, Subscription


class AlphabeticalFilter(admin.SimpleListFilter):
    """Отфильтровывает поле по алфавиту."""

    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

    @classmethod
    def setup(cls, field):
        """Настройка класса для использования в ModelAdmin.list_filter."""
        attrs = dict(parameter_name=field, title=field)
        return type("cls.__name__" + field, (cls,), attrs)

    def lookups(self, request, model_admin):
        """Возвращает список кортежей.
        Первый элемент используется в URL.
        Второй элемент служит для отображения в правой боковой панели.
        """
        queryset = model_admin.get_queryset(request)
        for char in self.ALPHABET:
            if queryset.filter(
                (f"{self.parameter_name}__istartswith", char),
            ).exists():
                yield (char, f"на {char}")

    def queryset(self, request, queryset):
        """Возвращает отфильтрованный queryset."""
        if self.value():
            return queryset.filter(
                (f"{self.parameter_name}__istartswith", self.value()),
            )
        return None


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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
    date_hierarchy = "date_joined"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Настройка админ-панели для модели связи рецепт-ингредиент."""

    list_display = ("pk", "author", "subscriber")
