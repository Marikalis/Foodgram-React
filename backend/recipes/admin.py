from django.contrib import admin

from .models import Ingredient, Recipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'favorites')
    list_filter = ('name', 'author', 'tags')

    def favorites(self, obj):
        return obj.favorites.count()
