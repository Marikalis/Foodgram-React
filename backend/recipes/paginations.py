
from rest_framework.pagination import PageNumberPagination


class QueryParamLimitPagination(PageNumberPagination):
    page_size_query_param = 'limit'
