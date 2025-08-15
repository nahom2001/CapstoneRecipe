from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("", views.api_menu, name='api-menu'),
    path("recipe-list/", views.recipe_list, name="recipe-list"),
    path("recipe-detail/<str:pk>/", views.recipe_detail, name="task-detail"),
    path("recipe-create", views.recipe_create, name="recipe-create"),
    path("recipe-update/<str:pk>/", views.recipe_update, name="recipe-update"),
    path("recipe-delete/<str:pk>/", views.recipe_delete, name="recipe-delete"),
    path("category-create", views.category_create, name="category-create"),
    path("recipe-category/<str:category_name>/", views.recipe_category, name="recipe-category"),
    path("recipe-ingredient/<str:ingredient>/", views.recipe_ingredient, name="recipe-ingredient"),
    
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
