from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Recipe(models.Model):
    """Модель рецептов."""

    name = models.CharField(max_length=200, verbose_name="Название")
    tags = models.ManyToManyField("Tags", verbose_name="Теги")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
    )
    ingredients = models.ManyToManyField(
        "Ingredients", verbose_name="Ингредиенты"
    )
    image = models.ImageField(verbose_name="Картинка")
    text = models.TextField(verbose_name="Текстовое описание")
    cooking_time = models.IntegerField(verbose_name="Время приготовления")
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
