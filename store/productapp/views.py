from typing import Any

from rest_framework.serializers import Serializer

from .models import Tag, Product, Review
from .serializers import TagsSerializer, ProductSerializer, ReviewSerializer

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, get_object_or_404, ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class TagsView(ListAPIView):
	"""
	Вывод списка тегов.
	"""
	queryset = Tag.objects.all()
	serializer_class = TagsSerializer


class ProductView(RetrieveAPIView):
	"""
	Вывод данных товара.
	"""
	queryset = (
		Product.objects
		.prefetch_related('images', 'tags', 'reviews', 'specifications')
		.select_related('category')
		.filter(archived=False)
	)
	serializer_class = ProductSerializer


class ProductReviewView(CreateAPIView):
	"""
	Создание отзыва к товару.
	"""
	queryset = (
		Review.objects
		.select_related('product')
		.all()
	)
	serializer_class = ReviewSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer: Serializer) -> None:
		"""
		Установка связи отзыва с товаром.

		:param serializer: Сериализатор
		:return: serializer.save(product=product)
		"""
		product = get_object_or_404(Product, id=self.kwargs['pk'], archived=False)
		return serializer.save(product=product)

	def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
		"""
		Создание отзыва и вывод списка отзывов к товару.

		:param request: Запрос
		:return: serialized.data
		"""
		# Создание отзыва родительским классом.
		super().create(request)

		# Вывод всего списка отзывов к товару.
		reviews_product = self.get_queryset().filter(product=self.kwargs['pk'])
		serialized = ReviewSerializer(reviews_product, many=True)

		return Response(data=serialized.data, status=status.HTTP_200_OK)
