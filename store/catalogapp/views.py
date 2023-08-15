from .models import Category
from .pagination import CustomPagination
from .serializers import CategorySerializer, CatalogSerializer, ProductSaleSerializer
from productapp.models import Product
from productapp.serializers import ProductSerializer

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView


class CategoryView(APIView):
	def get(self, request: Request) -> Response:
		categories = Category.objects.all()
		serialized = CategorySerializer(categories, many=True)

		return Response(data=serialized.data, status=status.HTTP_200_OK)


class CatalogView(ListAPIView):
	serializer_class = CatalogSerializer
	pagination_class = CustomPagination

	def get_queryset(self):
		queryset = Product.objects.all()

		name = self.request.query_params.get('filter[name]')
		if name is not None:
			queryset = queryset.filter(title__icontains=name)

		min_price = self.request.query_params.get('filter[minPrice]')
		if min_price is not None:
			queryset = queryset.filter(price__gte=min_price)

		max_price = self.request.query_params.get('filter[maxPrice]')
		if max_price is not None:
			queryset = queryset.filter(price__lte=max_price)

		free_delivery = self.request.query_params.get('filter[freeDelivery]')
		if free_delivery == 'true':
			queryset = queryset.filter(freeDelivery=True)

		available = self.request.query_params.get('filter[available]')
		if available == 'true':
			queryset = queryset.filter(count__gte=1)

		category = self.request.query_params.get('category')
		if category is not None:
			queryset = queryset.filter(category=category)

		tags = self.request.query_params.getlist('tags[]')
		if tags is not None:
			for id_tag in tags:
				queryset = queryset.filter(tags__id=id_tag)

		page = self.request.query_params.get('currentPage')
		if page is not None:
			pass
		return queryset

	def filter_queryset(self, queryset):
		sort = self.request.query_params.get('sort')
		sort_type = self.request.query_params.get('sortType')

		if sort_type == 'inc':
			if sort == 'price' or sort == 'reviews' or sort == 'rating':
				queryset = queryset.order_by('-' + sort)
			else:
				queryset = queryset.order_by('-date')
		else:
			if sort == 'price' or sort == 'reviews' or sort == 'rating':
				queryset = queryset.order_by(sort)
			else:
				queryset = queryset.order_by('date')

		return queryset


class ProductsPopularView(APIView):
	"""
	Популярные товары с сортировкой по рейтингу по убыванию.
	"""
	def get(self, request: Request) -> Response:
		products = Product.objects.all().order_by('-rating')
		serialized = CatalogSerializer(products, many=True)

		return Response(data=serialized.data, status=status.HTTP_200_OK)


class ProductsLimitedView(APIView):
	def get(self, request: Request) -> Response:
		products = Product.objects.filter(count__gte=1).order_by('count')
		serialized = CatalogSerializer(products, many=True)

		return Response(data=serialized.data, status=status.HTTP_200_OK)


class SaleView(ListAPIView):
	queryset = Product.objects.filter(salePrice__isnull=False)
	pagination_class = CustomPagination
	serializer_class = ProductSaleSerializer
