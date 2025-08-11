from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


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