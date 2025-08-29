# Recipe Management API 

Recipe Management API This is a REST full API using Django Rest Framework that categorizes and stores recipes and reviews, where functionalities include the usage of token authentication, filtering and ordering results, as well as testing with custom management for commands and images. This API enables you to add, retrieve, update, and remove recipe-related data, and is easy to integrate into any application for food lovers or cooking-related projects.

## Features

- Manage recipes, categories, and user reviews.
- Perform CRUD (Create, Read, Update, Delete) operations on all resources.
- Token-based authentication using JSON Web Tokens (JWT).
- Interactive API documentation via Swagger UI.
- Deployed on PythonAnywhere for easy access and testing.

## Technologies Used

- **Python**:  Core programming language.
- **Django REST Framework**: For building robust API endpoints.
- **drf-yasg**: For generating Swagger/OpenAPI documentation.
- **SQLite**: Default database (configurable for PostgreSQL or others).
- **PythonAnywhere**: Hosting platform for deployment.
- **Simple JWT**: For secure token-based authentication.


## Getting Started 


### Core Concepts

#### Authentication

- **JWT Tokens**: Users authenticate via JSON Web Tokens.
  - Obtain token: `/api/token/`
  - Refresh token: `/api/token/refresh/`
- **Custom User Model**: The API uses a custom user model to extend Django’s default authentication.

---

#### Models

1. **User**
   - Handles user registration and authentication.
   - Fields: username, email, password, and any custom fields added.

2. **Recipe**
   - Represents a recipe in the system.
   - Fields:
     - `title`
     - `description`
     - `ingredients` (list)
     - `instructions`
     - `category`
     - `preparation_time`
     - `cooking_time`
     - `servings`
     - `created_at`
     - `author` (foreign key to User)

---

#### API Endpoints

##### Authentication & Users

| Endpoint            | Method | Description |
|--------------------|--------|-------------|
| `/register/`        | POST   | Register a new user |
| `/api/token/`       | POST   | Obtain JWT token |
| `/api/token/refresh/` | POST | Refresh JWT token |

##### Recipes

| Endpoint                  | Method | Description |
|----------------------------|--------|-------------|
| `/recipes/`                | GET    | List all recipes (with pagination, filtering, and search) |
| `/recipes/`                | POST   | Create a new recipe (requires authentication) |
| `/recipes/<id>/`           | GET    | Retrieve details of a recipe |
| `/recipes/<id>/`           | PUT    | Update a recipe (owner only) |
| `/recipes/<id>/`           | DELETE | Delete a recipe (owner only) |

---

#### Features

1. **Filtering**
   - Filter recipes by `category` or `ingredient` via query parameters.
   - Example: `/recipes/?category=Dessert&ingredient=chocolate`

2. **Searching**
   - Search recipes by title or description.
   - Example: `/recipes/?search=chocolate`

3. **Pagination**
   - Lists are paginated to improve performance for large datasets.
   - Default page size and page query parameters are configurable.

4. **Permissions**
   - Only authenticated users can create, update, or delete recipes.
   - Users can only update or delete their own recipes.
   - Read operations are public.

---

#### Serializers

- **UserSerializer**: Handles user creation and authentication representation.
- **RecipeSerializer**: Handles recipe creation, updating, and detailed representation.
- Serializers validate data before saving to the database and control how data is returned in API responses.

---

#### Views

- **ViewSets**:
  - `RecipeViewSet` manages all CRUD operations for recipes.
  - Includes filtering, search, and pagination logic.
- **Mixins**:
  - Custom permission mixins ensure users only modify their own content.
- **Generic Views**:
  - Used for registration and other simple operations.

---

#### API Documentation

- Swagger UI is integrated for easy exploration and testing of endpoints.
- Access it at: `/swagger/`
- Includes automatic parameter validation, request/response schemas, and authentication handling.

---

## Setting up deployment

### Installation

1. **Clone the Repository**: 

- `git clone <repository-url>`
- `cd CapstoneRecipe`

2. **Setting Up a Virtual Environment**
Create and activate a virtual environment: 

- `python -m venv venv`
- `source venv/bin/activate`

3. **Install Dependencies**
Install the required Python packages: 

- `pip install -r requirements.txt` 

4. **Apply Database Migrations**
Setup teh database

- `python manage.py migrate`

5. **Adding Pythonanywhere's url to allowed hosts**
- In settings.py file, I added the url for pythonanywhere

`ALLOWED_HOSTS = ['nahomhulum.pythonanywhere.com']`

