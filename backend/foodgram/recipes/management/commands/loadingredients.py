import json
import os
import sys
from typing import Any, Optional

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


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
        try:
            os.chdir(settings.INGREDIENTS_JSON_DIR)
        except FileNotFoundError:
            print(
                "Файл не найден, проверьте путь INGREDIENTS_JSON_DIR,"
                " указанный в settings.py, на правильность."
            )
            sys.exit()

        with open("ingredients.json", "r", encoding="utf-8") as file:
            ingredient_list = json.load(file)
            count = 0
            number = len(ingredient_list)
            for ingredient in ingredient_list:
                Ingredient.objects.create(
                    name=ingredient["name"],
                    measurement_unit=ingredient["measurement_unit"],
                )
                count += 1
                print(f"В БД занесён {count}/{number} ингредиент")
        print("Команда закончила своё выполнение.")
