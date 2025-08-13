from django.shortcuts import render
from .models import Recipe
from .serializers import RecipeSummarySerializer, RecipeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status


# Create your views here.
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recipe_create(request):
    serializer = RecipeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
