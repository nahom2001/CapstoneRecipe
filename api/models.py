from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Recipe(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField()
    instructions = models.TextField(blank=False)
    prep_time = models.DurationField()
    cooking_time = models.DurationField()
    servings = models.DecimalField(max_digits=4, decimal_places=1, default=4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey('User', on_delete=CASCADE, related_name='recipes')

    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient', related_name='recipes', blank=False)
    categories = models.ManyToManyField('Category', related_name="recipes")


    def __str__(self):
        return self.title


class User(AbstractUser):
    pass
