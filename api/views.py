from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import render
from .models import Recipe, Ingredient, Category
from .serializers import RecipeSummarySerializer, RecipeSerializer, CategorySerializer, RegisterSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny 
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from .utils import filter_recipes, paginate_queryset
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .examples import (
    RECIPE_CREATE_REQUEST,
    RECIPE_CREATE_RESPONSE,
    RECIPE_UPDATE_REQUEST,
    RECIPE_UPDATE_RESPONSE,
    CATEGORY_CREATE_REQUEST,
    CATEGORY_CREATE_RESPONSE,
    RECIPE_DETAIL_RESPONSE,
    RECIPE_LIST_RESPONSE,
    CATEGORY_FILTER_RESPONSE,
    RECIPE_INGREDIENT_FILTER_RESPONSE
)





# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        operation_description="Obtain JWT token using form data",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True)
        ],
        responses={200: 'JWT token returned'}
    )
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
        'API List': '/api/register',
    }
    return Response(api_urls)



@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            'password2': openapi.Schema(type=openapi.TYPE_STRING, description='Confirm Password'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
        },
        required=['username', 'email', 'password', 'password2', 'first_name', 'last_name'],
        example={
            "username": "john_doe",
            "email": "john@example.com",
            "password": "securepassword123",
            "password2": "securepassword123",
            "first_name": "John",
            "last_name": "Doe"
        }
    ),
    responses={
        201: openapi.Response(
            description="User registered successfully",
            examples={"application/json": {
                "username": "john_doe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe"
            }}
        ),
        400: "Invalid data"
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="List of all recipes",
            examples={"application/json": RECIPE_LIST_RESPONSE}
        )
    }
)
@api_view(['GET'])
def recipe_list(request):
    recipes = Recipe.objects.all().order_by('id')
    filtered_recipes = filter_recipes(recipes, request.GET)
    paginated_recipes, paginator = paginate_queryset(filtered_recipes, request) 
    serializer = RecipeSummarySerializer(paginated_recipes, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="Recipe detail response",
            examples={"application/json": RECIPE_DETAIL_RESPONSE}
        ),
        404: "Recipe not found"
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recipe_detail(request, pk):
    recipe = Recipe.objects.get(id=pk)
    serializer = RecipeSerializer(recipe, many=False)
    return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            name='category_name',
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description='Name of the category to filter by'
        )
    ],
    responses={
        200: openapi.Response(
            description="Recipes by category",
            examples={"application/json": {"category": {"name": "Dessert"}, "recipes": CATEGORY_FILTER_RESPONSE}}
        ),
        404: "Category not found"
    }
)


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

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            name='ingredient',
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            description='Name (partial or full) of the ingredient to filter by'
        )
    ],
    responses={
        200: openapi.Response(
            description="Recipes by ingredient name",
            examples={"application/json": {
                "ingredient": {
                    "query": "Cocoa",
                    "matched": ["Cocoa Powder"]
                },
                "recipes": RECIPE_INGREDIENT_FILTER_RESPONSE
            }}
        ),
        404: "Ingredient not found"
    }
)
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

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        example=RECIPE_CREATE_REQUEST
    ),
    responses={
        201: openapi.Response(
            description="Recipe created successfully",
            examples={"application/json": RECIPE_CREATE_RESPONSE}
        ),
        400: "Invalid data"
    }
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recipe_create(request):
    serializer = RecipeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        example=CATEGORY_CREATE_REQUEST
    ),
    responses={
        201: openapi.Response(
            description="Category created successfully",
            examples={"application/json": CATEGORY_CREATE_RESPONSE}
        ),
        400: "Invalid data"
    }
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        example=RECIPE_UPDATE_REQUEST
    ),
    responses={
        200: openapi.Response(
            description="Recipe updated successfully",
            examples={"application/json": RECIPE_UPDATE_RESPONSE}
        ),
        400: "Invalid data",
        403: "Forbidden"
    }
)

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
