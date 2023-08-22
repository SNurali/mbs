from django.db.models import QuerySet
from datetime import datetime

from .models import Category
from .pagination import CatalogPagination
from .serializers import CategorySerializer, CatalogSerializer, CatalogSaleSerializer
from productapp.models import Product

from rest_framework.generics import ListAPIView


class CategoryView(ListAPIView):
	"""
	Список родительских категорий и их подкатегорий.
	"""
	queryset = (
		Category.objects
		.select_related('parent')
		.filter(parent__isnull=True, archived=False)
	)
	serializer_class = CategorySerializer


class CatalogView(ListAPIView):
	"""
	Каталог товаров.
	"""
	serializer_class = CatalogSerializer
	pagination_class = CatalogPagination

	def get_queryset(self) -> QuerySet:
		"""
		Фильтрация товаров.

		:return: queryset
		"""
		# Список товаров.
		queryset = (
			Product.objects
			.select_related('category')
			.prefetch_related('images', 'tags', 'reviews')
			.filter(archived=False)
		)

		# Получение параметров.
		params = self.request.query_params
		name = params.get('filter[name]')
		min_price = params.get('filter[minPrice]')
		max_price = params.get('filter[maxPrice]')
		free_delivery = params.get('filter[freeDelivery]')
		available = params.get('filter[available]')
		category = params.get('category')
		tags = params.getlist('tags[]')

		# Фильтр товаров по параметрам.
		if name is not None:
			queryset = queryset.filter(title__icontains=name)
		if min_price is not None:
			queryset = queryset.filter(price__gte=min_price)
		if max_price is not None:
			queryset = queryset.filter(price__lte=max_price)
		if free_delivery == 'true':
			queryset = queryset.filter(freeDelivery=True)
		if available == 'true':
			queryset = queryset.filter(count__gte=1)
		if category is not None:
			queryset = queryset.filter(category=category)
		if tags is not None:
			for id_tag in tags:
				queryset = queryset.filter(tags__id=id_tag)

		return queryset

	def filter_queryset(self, queryset) -> QuerySet:
		"""
		Сортировка товаров.

		:param queryset: Товары
		:return: queryset
		"""
		sort = self.request.query_params.get('sort')
		sort_type = self.request.query_params.get('sortType')
		sort_types = ('price', 'reviews', 'rating')

		# Сортировка по убыванию. Если не указан тип сортировки, то сортировка по дате.
		if sort_type == 'inc':
			if sort in sort_types:
				queryset = queryset.order_by('-' + sort)
			else:
				queryset = queryset.order_by('-date')
		else:
			# Сортировка по возрастанию. Если не указан тип сортировки, то сортировка по дате.
			if sort in sort_types:
				queryset = queryset.order_by(sort)
			else:
				queryset = queryset.order_by('date')

		return queryset


class ProductsPopularView(ListAPIView):
	"""
	Список первых 8 популярных товаров.
	Сортировка по рейтингу от большего к меньшему либо по кол-ву продаж.
	"""
	queryset = (
		Product.objects
		.select_related('category')
		.prefetch_related('images', 'tags', 'reviews')
		.filter(count__gte=1, archived=False)
		.order_by('-rating', 'salesCount')
	)[:8]
	serializer_class = CatalogSerializer


class ProductsLimitedView(ListAPIView):
	"""
	Список первых 16 заканчивающихся товаров.
	Сортировка по кол-ву от меньшего к большему либо по кол-ву продаж.
	"""
	queryset = (
		Product.objects
		.select_related('category')
		.prefetch_related('images', 'tags', 'reviews')
		.filter(count__gte=1, archived=False)
		.order_by('count', 'salesCount')
	)[:16]
	serializer_class = CatalogSerializer


class SaleView(ListAPIView):
	"""
	Список первых 8 товаров с ценой по акции.
	Сортировка по кол-ву продаж.
	"""
	queryset = (
		Product.objects
		.select_related('category')
		.prefetch_related('images', 'tags', 'reviews')
		.filter(
			count__gte=1,
			salePrice__isnull=False,
			dateFrom__lte=datetime.now().date(),
			dateTo__gte=datetime.now().date(),
			archived=False
		)
		.order_by('salesCount')
	)[:8]
	pagination_class = CatalogPagination
	serializer_class = CatalogSaleSerializer
