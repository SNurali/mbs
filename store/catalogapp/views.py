from rest_framework.pagination import PageNumberPagination

from .models import Category
from .serializers import CategorySerializer, CatalogSerializer
from productapp.models import Product

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


class CategoryView(APIView):
	def get(self, request: Request) -> Response:
		categories = Category.objects.all()
		serialized = CategorySerializer(categories, many=True)

		return Response(data=serialized.data, status=status.HTTP_200_OK)


# кастомная пагинация
class CustomPagination(PageNumberPagination):
	def get_paginated_response(self, data):
		return Response({
			'items': data,
			'currentPage': self.get_next_link(),
			'lastPage': self.get_previous_link(),
		})


class CatalogView(APIView):
	pagination_class = CustomPagination

	def get(self, request: Request) -> Response:
		products = Product.objects.all()
		serialized = CatalogSerializer(products, many=True)

		return Response(data=serialized.data, status=status.HTTP_200_OK)
