from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import render
from .models import Recipe
from .serializers import RecipeSummarySerializer, RecipeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    parser_classes = [FormParser, MultiPartParser]  # Accept form data
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



@api_view(['GET'])
def api_menu(request):
    api_urls = {
        'List Recipes': '/api/recipe-list/',
        'Recipe Detail': '/api/recipe-detail/{id}/',
        'Create Recipe': '/api/recipe-create/',
        'Update Recipe': '/api/recipe-update/{id}/',
        'Delete Recipe': '/api/recipe-delete/{id}/',
        'Get Recipe by Category': '/api/recipe-category/{category_name}/',
        'Get Recipe by Ingredient': '/api/recipe-ingredient/{ingredient}/',
        'Create Category': '/api/category-create/',
        'Token Creation': '/api/token/',
        'Token Refresh': '/api/token/refresh/',
        'API List': '/api/'
    }
    return Response(api_urls)

@api_view(['GET'])
def recipe_list(request):
    recipes = Recipe.objects.all().order_by('id')
    serializer = RecipeSummarySerializer(recipes, many=True)
    return Response(serializer.data)  # Return serialized data instead of raw queryset

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recipe_detail(request, pk):
    recipe = Recipe.objects.get(id=pk)
    serializer = RecipeSerializer(recipe, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def recipe_category(request, category_name):
    try:
        category = Category.objects.get(category_name__iexact=category_name)
    except Category.DoesNotExist:
        return Response({"detail": "Category not found."}, status=404)

    recipes = category.recipes.all()
    serializer = RecipeSerializer(recipes, many=True)

    return Response({
        "category": {
            "name": category.category_name
        },
        "recipes": serializer.data
    })

@api_view(['GET'])
def recipe_ingredient(request, ingredient):
    try:
        ingredients = Ingredient.objects.filter(name__icontains=ingredient)
    except Ingredient.DoesNotExist:
        return Response({"detail": "Ingredient not found."}, status=404)

    recipes = Recipe.objects.filter(recipeingredient__ingredient__in=ingredients).distinct()
    serializer = RecipeSerializer(recipes, many=True)

    return Response({
        "ingredient": {
            "query": ingredient,
            "matched": [ing.name for ing in ingredients]
        },
        "recipes": serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recipe_create(request):
    serializer = RecipeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def recipe_update(request, pk):
    recipe = Recipe.objects.get(id=pk)

    if recipe.user != request.user:
        return Response({'detail': 'You do not have permission to update this recipe.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    serializer = RecipeSerializer(instance=recipe, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def recipe_delete(request, pk):
    recipe = Recipe.objects.get(id=pk)

    if recipe.user != request.user:
        return Response({'detail': 'You do not have permission to update this recipe.'}, status=status.HTTP_403_FORBIDDEN)

    recipe.delete()

    return Response('Recipe successfully deleted!')
