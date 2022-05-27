from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'recipes'

router_v1 = DefaultRouter()

router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router_v1.urls)),
]
