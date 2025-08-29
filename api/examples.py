# ------------------------
# Category Endpoints
# ------------------------

CATEGORY_CREATE_REQUEST = {
    "category_name": "Dessert"
}

CATEGORY_CREATE_RESPONSE = {
    "category_name": "Dessert"
}

CATEGORY_FILTER_REQUEST = "Dessert"

CATEGORY_FILTER_RESPONSE = {
    "category": {
        "name": "Dessert"
    },
    "recipes": [
        {
            "id": 1,
            "title": "Chocolate Cake",
            "description": "Rich chocolate cake with ganache",
            "instructions": "Mix, bake, and chill",
            "prep_time": "20:00",
            "cooking_time": "30:00",
            "servings": "8",
            "categories": {
                "name": "Dessert"
            },
            "recipe_ingredients": [
                {
                    "ingredient": {"id": 1, "name": "Flour"},
                    "quantity": 2,
                    "unit": "cups"
                }
            ]
        }
    ]
}

# ------------------------
# Recipe Endpoints
# ------------------------

RECIPE_CREATE_REQUEST = {
    "title": "Chocolate Cake",
    "description": "Delicious and moist chocolate cake",
    "instructions": "1. Mix dry ingredients\n2. Add wet ingredients\n3. Bake at 180°C for 30 minutes",
    "prep_time": "20:00",
    "cooking_time": "30:00",
    "servings": "8",
    "categories": [
        {"category_name": "Dessert"}
    ],
    "recipe_ingredients": [
        {
            "ingredient": {"name": "Flour"},
            "quantity": 2,
            "unit": "cups"
        },
        {
            "ingredient": {"name": "Cocoa Powder"},
            "quantity": 0.5,
            "unit": "cups"
        }
    ]
}

RECIPE_CREATE_RESPONSE = {
    "id": 1,
    "title": "Chocolate Cake",
    "description": "Delicious and moist chocolate cake",
    "instructions": "1. Mix dry ingredients\n2. Add wet ingredients\n3. Bake at 180°C for 30 minutes",
    "prep_time": "20:00",
    "cooking_time": "30:00",
    "servings": "8",
    "categories": ["Dessert"],
    "recipe_ingredients": [
        {
            "ingredient": {"id": 1, "name": "Flour"},
            "quantity": 2,
            "unit": "cups"
        },
        {
            "ingredient": {"id": 2, "name": "Cocoa Powder"},
            "quantity": 0.5,
            "unit": "cups"
        }
    ]
}

RECIPE_LIST_RESPONSE = [
    {
        "id": 1,
        "title": "Chocolate Cake",
        "description": "Delicious and moist chocolate cake",
        "prep_time": "20:00",
        "cooking_time": "30:00",
        "servings": "8",
        "categories": ["Dessert"]
    },
    {
        "id": 2,
        "title": "Vanilla Pancakes",
        "description": "Fluffy vanilla pancakes",
        "prep_time": "10:00",
        "cooking_time": "15:00",
        "servings": "4",
        "categories": ["Breakfast"]
    }
]

RECIPE_DETAIL_RESPONSE = RECIPE_CREATE_RESPONSE

RECIPE_UPDATE_REQUEST = {
    "title": "Ultimate Chocolate Cake",
    "description": "With chocolate ganache topping",
    "prep_time": "25:00",
    "cooking_time": "35:00",
    "servings": "10"
}

RECIPE_UPDATE_RESPONSE = {
    **RECIPE_CREATE_RESPONSE,
    "title": "Ultimate Chocolate Cake",
    "description": "With chocolate ganache topping",
    "prep_time": "25:00",
    "cooking_time": "35:00",
    "servings": "10"
}

RECIPE_DELETE_RESPONSE = {
    "detail": "Recipe successfully deleted!"
}

# --------------------------
# Ingredient Filter Endpoint
# --------------------------

RECIPE_INGREDIENT_FILTER_REQUEST = "Cocoa Powder"

RECIPE_INGREDIENT_FILTER_RESPONSE = {
    "ingredient": {
        "query": "Cocoa Powder",
        "matched": ["Cocoa Powder"]
    },
    "recipes": [
        {
            "id": 1,
            "title": "Chocolate Cake",
            "description": "Delicious and moist chocolate cake",
            "instructions": "Mix ingredients, bake, and cool",
            "prep_time": "20:00",
            "cooking_time": "30:00",
            "servings": "8",
            "categories": ["Dessert"],
            "recipe_ingredients": [
                {
                    "ingredient": {"id": 2, "name": "Cocoa Powder"},
                    "quantity": 0.5,
                    "unit": "cups"
                }
            ]
        }
    ]
}

# --------------------------
# Authentication Endpoints
# --------------------------

TOKEN_OBTAIN_REQUEST = {
    "username": "user123",
    "password": "securepassword"
}

TOKEN_OBTAIN_RESPONSE = {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOi...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
}

TOKEN_REFRESH_REQUEST = {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
}

TOKEN_REFRESH_RESPONSE = {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
}
