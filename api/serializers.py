from rest_framework import serializers
from .models import Ingredient, Recipe, Category, RecipeIngredient

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']




class RecipeSummarySerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        slug_field='category_name',
        read_only=True
    )

    class Meta:
        model = Recipe 
        fields = ['id', 'title', 'description', 'prep_time', 'cooking_time', 'servings', 'categories']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']

class RecipeSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)  # nested categories
    recipe_ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'instructions', 'prep_time', 'cooking_time', 'servings', 'categories', 'recipe_ingredients']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        ingredients_data = validated_data.pop('recipeingredient_set', [])

        recipe = Recipe.objects.create(**validated_data)

        # Create/get categories dynamically
        categories = []
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            categories.append(category)
        recipe.categories.set(categories)

        for item in ingredients_data:
            ingredient_data = item.pop('ingredient')
            ingredient, created = Ingredient.objects.get_or_create(**ingredient_data)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, **item)

        return recipe

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', None)
        ingredients_data = validated_data.pop('recipeingredient_set', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if categories_data is not None:
            categories = []
            for category_data in categories_data:
                category, created = Category.objects.get_or_create(**category_data)
                categories.append(category)
            instance.categories.set(categories)

        instance.recipeingredient_set.all().delete()
        for item in ingredients_data:
            ingredient_data = item.pop('ingredient')
            ingredient, created = Ingredient.objects.get_or_create(**ingredient_data)
            RecipeIngredient.objects.create(recipe=instance, ingredient=ingredient, **item)

        return instance
