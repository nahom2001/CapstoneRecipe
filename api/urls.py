from django.urls import path
from . import views

urlpatterns = [
    path("", views.api_menu, name='api-menu'),
    path("recipe-list/", views.recipe_list, name="recipe-list"),
    path("recipe-detail/<str:pk>/", views.recipe_detail, name="task-detail"),
    path("recipe-create", views.recipe_create, name="recipe-create"),
]
