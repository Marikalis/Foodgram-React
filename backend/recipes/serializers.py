from rest_framework import serializers

from users.serializers import UserSerializer
from .fields import Base64StrToFile
from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64StrToFile()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and Favorite.objects.filter(
                user__id=user.id,
                recipe__id=recipe.id
            ).exists()
        )

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and ShoppingCart.objects.filter(
                user__id=user.id,
                recipe__id=recipe.id
            ).exists()
        )

    def get_ingredients(self, recipe):
        recipes = IngredientInRecipe.objects.filter(recipe=recipe)
        serializer = IngredientInRecipeSerializer(recipes, many=True)
        return serializer.data

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше или равно минуте.'
            )
        return cooking_time

    def preprocess_ingredients(self):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                'Поле "ingredients" обязательное.'
            )
        result_ingredients = []
        pks = []
        for ingredient in ingredients:
            pk = ingredient.get('id')
            amount = ingredient.get('amount')
            if not pk or not amount:
                raise serializers.ValidationError(
                    'Ингредиенты заполнены некорректно.'
                )
            try:
                result_ingredient = Ingredient.objects.get(id=pk)
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    f'Ингредиент(id={pk}) не существует.'
                )
            if pk in pks:
                raise serializers.ValidationError(
                    f'Повторный ингредиент: id={pk}'
                )
            pks.append(pk)
            try:
                amount = int(amount)
            except ValueError:
                raise serializers.ValidationError(
                    '"amount" должно быть целым числом.'
                )
            if amount < 1:
                raise serializers.ValidationError(
                    '"amount" должно быть больше или равно единице.'
                )
            result_ingredients.append((result_ingredient, amount))
        return result_ingredients

    def preprocess_tags(self):
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError('Поле "tags" обязательное.')
        result_tags = []
        for pk in tags:
            try:
                tag = Tag.objects.get(id=pk)
            except Tag.DoesNotExist:
                raise serializers.ValidationError(
                    f'Тег(id={pk}) не существует.'
                )
            result_tags.append(tag)
        return result_tags

    def preprocess_recipe(self, recipe):
        ingredients = self.preprocess_ingredients()
        tags = self.preprocess_tags()
        recipe.tags.set(tags)
        recipe.save()
        for ingredient, amount in ingredients:
            IngredientInRecipe.objects.create(
                amount=amount, ingredient=ingredient, recipe=recipe
            )
        return recipe

    def create(self, validated_data):
        recipe = Recipe.objects.create(**validated_data)
        return self.preprocess_recipe(recipe)

    def update(self, recipe, validated_data):
        ingredients_in_recipe = IngredientInRecipe.objects.filter(
            recipe__id=recipe.id
        )
        ingredients_in_recipe.delete()
        recipe = self.preprocess_recipe(recipe)
        return super().update(recipe, validated_data)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )
