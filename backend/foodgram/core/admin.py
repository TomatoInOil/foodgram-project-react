from django.contrib import admin


class AlphabeticalFilter(admin.SimpleListFilter):
    """Отфильтровывает поле по алфавиту."""

    ALPHABET = (
        "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    )

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
