from enum import Enum

from django_filters import rest_framework as fl
from django_filters.filters import (
    AllValuesMultipleFilter,
    ModelChoiceFilter,
    NumberFilter
)

from users.models import User
from .models import Recipe


class IsInFavorites(Enum):
    IN = 1
    OUT = 0


class IsInShoppingCart(Enum):
    IN = 1
    OUT = 0


class RecipeFilter(fl.FilterSet):
    author = ModelChoiceFilter(queryset=User.objects.all())
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = NumberFilter(method='get_is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == IsInFavorites.IN.value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == IsInShoppingCart.IN.value and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')
