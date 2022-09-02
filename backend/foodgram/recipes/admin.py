from django.contrib import admin

from recipes.models import Ingredient, Recipe, Tag, IngredientQuantity

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(IngredientQuantity)
