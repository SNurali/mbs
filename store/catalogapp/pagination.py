from rest_framework import pagination
from rest_framework.response import Response


class CatalogPagination(pagination.PageNumberPagination):
    """
    Кастомизированная пагинация для каталога товаров.
    """
    page_query_param = 'currentPage'
    page_size = 20
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages,
        })
