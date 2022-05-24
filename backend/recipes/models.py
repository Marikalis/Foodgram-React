from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

AMOUNT_GREATER_ZERO = 'Количество должно быть больше нуля.'
COOKING_TIME_GREATER_ONE = 'Время приготовления должно быть больше минуты.'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=100, unique=True
    )
    color = models.CharField(verbose_name='Цвет', max_length=50, unique=True)
    slug = models.SlugField(
        verbose_name='Название-метка', max_length=100, unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=100, unique=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения', max_length=20
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(verbose_name='Название', max_length=200)
    ingredients = models.ManyToManyField(
        Ingredient, related_name='recipes',
        verbose_name='Ингредиенты', through='IngredientInRecipe'
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги',
    )
    text = models.TextField(verbose_name='Описание', max_length=800)
    image = models.ImageField(
        verbose_name='Картинка', upload_to='recipe_images'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[MinValueValidator(1, message=COOKING_TIME_GREATER_ONE)]
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт'
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, message=AMOUNT_GREATER_ZERO)
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [models.UniqueConstraint(
            fields=['ingredient', 'recipe'],
            name='unique_ingredient'
        )]


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorite'
        )]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_shopping_cart'
        )]
