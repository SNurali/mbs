from django.shortcuts import render
import json

from productapp.models import Product
from catalogapp.serializers import CatalogSerializer

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


class BasketView(APIView):
	def get(self, request: Request) -> Response:
		data = []
		basket = request.session.get('basket')

		for item in sorted(basket.keys()):
			product = Product.objects.get(pk=item)
			product.count = request.session['basket'][item]
			serialized = CatalogSerializer(product)
			data.append(serialized.data)

		return Response(data=data, status=status.HTTP_200_OK)

	def post(self, request: Request) -> Response:
		data = json.loads(request.body)
		id_product = str(data['id'])
		count_product = data['count']
		basket = request.session.get('basket')

		# создание корзины в сессии если ее нет
		if not basket:
			basket = request.session['basket'] = {}

		# создание товара в сессии если его нет
		if not id_product in basket.keys():
			basket[id_product] = 0

		# проверка наличия товара
		product = Product.objects.get(pk=id_product)

		if basket[id_product] + count_product > product.count:
			basket[id_product] = product.count
		else:
			basket[id_product] += count_product

		# сохранение сессии
		request.session.modified = True

		# вывод корзины из сессии с кол-вом для заказа
		data = []

		for item in sorted(basket.keys()):
			product = Product.objects.get(pk=item)
			product.count = basket[str(item)]
			serialized = CatalogSerializer(product)
			data.append(serialized.data)

		return Response(data=data, status=status.HTTP_200_OK)

	def delete(self, request: Request) -> Response:
		data = json.loads(request.body)
		id_product = str(data['id'])
		count_product = data['count']
		basket = request.session['basket']

		# проверка кол-ва товара в сессии и удаление либо уменьшение кол-ва
		if count_product >= basket.get(id_product):
			del basket[id_product]
		else:
			basket[id_product] -= count_product

		# обновление сессии
		request.session.modified = True

		# вывод корзины из сессии с кол-вом для заказа
		data = []

		for item in sorted(basket.keys()):
			product = Product.objects.get(pk=item)
			product.count = basket[str(item)]
			serialized = CatalogSerializer(product)
			data.append(serialized.data)

		return Response(data=data, status=status.HTTP_200_OK)
