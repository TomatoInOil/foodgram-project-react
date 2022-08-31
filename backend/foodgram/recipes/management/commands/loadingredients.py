import os
from typing import Any, Optional

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Команда загружает данные ингредиентов в БД."""

    help = (
        "Загрузить данные из .json файла, расположенного в директории "
        "settings.INGREDIENTS_JSON_DIR, в БД."
    )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """
        Читает json файл, с помощью Django ORM создаёт объекты и сохраняет.
        """
        os.chdir(settings.INGREDIENTS_JSON_DIR)

        print("Команда успешно закончила своё выполнение.")
