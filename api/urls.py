from django.urls import path
from . import views

urlpatterns = [
    path("", views.api_menu, name='api-menu'),
    path("recipe-list/", views.recipe_list, name="recipe-list"),
]
