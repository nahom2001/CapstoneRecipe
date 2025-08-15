from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

def filter_recipes(queryset, params):
    search_query = params.get('search')
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(categories__category_name__icontains=search_query)
        )

    prep_time = params.get('prep_time')
    if prep_time:
        queryset = queryset.filter(prep_time=prep_time)

    cooking_time = params.get('cooking_time')
    if cooking_time:
        queryset = queryset.filter(cooking_time=cooking_time)

    servings = params.get('servings')
    if servings:
        queryset = queryset.filter(servings=servings)
        
    return queryset


def paginate_queryset(queryset, request, page_size=3):
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginated_qs = paginator.paginate_queryset(queryset, request)
    return paginated_qs, paginator
