import json

from productapp.models import Product
from catalogapp.serializers import CatalogSerializer

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


class BasketView(APIView):
	"""
	Корзина для покупки товаров.
	"""
	def get(self, request: Request) -> Response:
		"""
		Вывод списка товаров в корзине.

		:param request: Запрос
		:return: data
		"""
		data = []

		# Берем корзину из сессии.
		basket = request.session.get('basket')

		# Если корзина существует, то выводим товары.
		if basket:
			for item in sorted(basket.keys()):
				product = (
					Product.objects
					.select_related('category')
					.prefetch_related('images', 'tags', 'reviews')
					.get(pk=item, archived=False)
				)

				# Указываем кол-во товара для заказа из сессии.
				product.count = request.session['basket'][item]
				serialized = CatalogSerializer(product)
				data.append(serialized.data)

		return Response(data=data, status=status.HTTP_200_OK)

	def post(self, request: Request) -> Response:
		"""
		Добавление товара в корзину.

		:param request: Запрос
		:return: data
		"""
		data = json.loads(request.body)
		id_product = str(data['id'])
		count_product = data['count']

		# Создание корзины в сессии если ее нет.
		basket = request.session.get('basket')
		if not basket:
			basket = request.session['basket'] = {}

		# Создание товара в сессии если его нет.
		if not id_product in basket.keys():
			basket[id_product] = 0

		# Проверка наличия товара
		product = Product.objects.get(pk=id_product, archived=False)

		# Кол-во товара в корзине и добавляемое кол-во больше кол-ва в наличии, то ограничиваем по наличию.
		if basket[id_product] + count_product > product.count:
			basket[id_product] = product.count
		else:
			basket[id_product] += count_product

		# Сохранение сессии.
		request.session.modified = True

		# Вывод корзины из сессии с кол-вом для заказа.
		data = []

		for item in sorted(basket.keys()):
			product = (
				Product.objects
				.select_related('category')
				.prefetch_related('images', 'tags', 'reviews')
				.get(pk=item, archived=False)
			)

			# Берем кол-во товара из сессии корзины.
			product.count = basket[str(item)]
			serialized = CatalogSerializer(product)
			data.append(serialized.data)

		return Response(data=data, status=status.HTTP_200_OK)

	def delete(self, request: Request) -> Response:
		data = json.loads(request.body)
		id_product = str(data['id'])
		count_product = data['count']
		basket = request.session['basket']

		# Проверка кол-ва товара в сессии и удаление либо уменьшение кол-ва.
		if count_product >= basket.get(id_product):
			del basket[id_product]
		else:
			basket[id_product] -= count_product

		# Обновление сессии.
		request.session.modified = True

		# Вывод корзины из сессии с кол-вом для заказа.
		data = []

		for item in sorted(basket.keys()):
			product = (
				Product.objects
				.select_related('category')
				.prefetch_related('images', 'tags', 'reviews')
				.get(pk=item, archived=False)
			)
			product.count = basket[str(item)]
			serialized = CatalogSerializer(product)
			data.append(serialized.data)

		return Response(data=data, status=status.HTTP_200_OK)
