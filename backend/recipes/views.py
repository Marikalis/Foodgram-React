from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)

RECIPE_ALREADY_IN_SHOPPING_CART = 'Рецепт уже в корзине!'
RECIPE_NOT_IN_SHOPPING_CART = 'Рецепта нет в корзине!'
RECIPE_ALREADY_IN_FAVORITES = 'Вы уже добавили рецепт в избранное!'
RECIPE_NOT_IN_FAVORITES = 'Рецепта нет в избранных!'
RECIPE_NOT_EXISTS = 'Рецепт не существует!'


class IngredientViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def favorite_or_cart(self, request, id, model, message_not_in, message_in,
                         class_serializer):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if request.method == 'DELETE':
            obj = model.objects.filter(recipe=recipe, user=user).first()
            if not obj:
                return Response(
                    data={'errors': message_not_in},
                    status=status.HTTP_400_BAD_REQUEST
                )
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if model.objects.filter(recipe=recipe, user=user).exists():
            return Response(
                data={'errors': message_in},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = class_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=('POST', 'DELETE'), detail=False,
            url_path=r'(?P<id>\d+)/favorite',
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, id):
        return self.favorite_or_cart(
            request, id, Favorite, RECIPE_NOT_IN_FAVORITES,
            RECIPE_ALREADY_IN_FAVORITES, FavoriteSerializer
        )

    @action(methods=('POST', 'DELETE'), detail=False,
            url_path=r'(?P<id>\d+)/shopping_cart',
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, id):
        return self.favorite_or_cart(
            request, id, ShoppingCart, RECIPE_NOT_IN_SHOPPING_CART,
            RECIPE_ALREADY_IN_SHOPPING_CART, ShoppingCartSerializer
        )

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        cart = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user).values(
                'ingredient__name', 'ingredient__measurement_unit').annotate(
                    count=Sum('amount'))
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="cart.txt"'
        for ingredient in cart:
            row = '{} - {} {}\n'.format(
                ingredient['ingredient__name'],
                ingredient['count'],
                ingredient['ingredient__measurement_unit'])
            response.write(row)
        return response
