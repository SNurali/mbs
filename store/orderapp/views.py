import json

from orderapp.models import Order, ProductOrder
from .serializers import OrderSerializer
from profileapp.models import Profile
from productapp.models import Product
from .models import Delivery

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class OrdersView(APIView):
	"""
	Список заказов и создание заказа.
	"""
	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:
		"""
		Вывод списка заказов пользователя по профилю.

		:param request: Запрос
		:return: serialized.data
		"""
		orders = (
			Order.objects
			.select_related('profile')
			.filter(profile=request.user.profile.pk, archived=False)
			.order_by('-createdAt')
		)
		serialized = OrderSerializer(orders, many=True)

		return Response(data=serialized.data, status=status.HTTP_200_OK)

	def post(self, request: Request) -> Response:
		"""
		Создание нового заказа.

		:param request: Запрос
		:return: {'orderId': order.pk}
		"""
		data_products = json.loads(request.body)
		profile = Profile.objects.get(pk=request.user.profile.pk, archived=False)

		free_delivery = True
		order_cost = 0

		# Проверка у каждого товара бесплатной доставки и подсчет суммы заказа.
		for product in data_products:
			order_cost += product['count'] * product['price']

			# Если у какого-либо товара не бесплатная доставка, то флаг free_delivery = False.
			if product['freeDelivery'] == False:
				free_delivery = False

		# Проверка есть ли доставка где maxCost больше суммы заказа
		get_delivery = Delivery.objects.filter(maxCost__gte=order_cost)

		# Если все товары бесплатные в доставке, то бесплатная доставка.
		if free_delivery:
			delivery = 'free'
		# Если не попадаем под условия доставки, то бесплатная доставка.
		elif not get_delivery:
			delivery = 'free'
		# Иначе обычная доставка.
		else:
			delivery = 'ordinary'

		# Создание заказа.
		order = Order.objects.create(
			profile=profile,
			deliveryType=delivery,
			totalCost=order_cost,
			fullName=profile.fullName,
			email=profile.email,
			phone=profile.phone,
		)

		# Создание связи каждого продукта к заказу с указанием кол-ва.
		for product in data_products:
			get_product = Product.objects.get(pk=product['id'], archived=False)
			ProductOrder.objects.create(
				orderId=order,
				productId=get_product,
				count=product['count']
			)

		# Обнуление корзины после создания заказа.
		request.session['basket'] = {}
		request.session.modified = True

		return Response(data={'orderId': order.pk}, status=status.HTTP_200_OK)


class OrderView(APIView):
	"""
	Заказ с товарами.
	"""
	permission_classes = [IsAuthenticated]

	def get(self, request: Request, pk) -> Response:
		"""
		Вывод данных заказа.

		:param request: Запрос
		:param pk: Идентификатор заказа
		:return: serialized.data
		"""
		order = (
			Order.objects
			.prefetch_related('products')
			.get(pk=pk, archived=False)
		)
		serialized = OrderSerializer(order)

		return Response(data=serialized.data, status=status.HTTP_200_OK)

	def post(self, request: Request, pk) -> Response:
		"""
		Обновление данных заказа.

		:param request: Запрос
		:param pk: Идентификатор заказа
		:return: {'orderId': order.pk}
		"""
		data = json.loads(request.body)
		delivery_name = data['deliveryType']
		order_cost = data['totalCost']

		# Если доставка заказа не бесплатная, то добавление стоимости доставки к сумме заказа.
		if delivery_name != 'free':
			delivery = Delivery.objects.get(name=delivery_name)
			if delivery:
				order_cost += delivery.deliveryPrice

		# Обновление данных заказа из введенных данных пользователя
		order = Order.objects.get(pk=pk, archived=False)
		order.fullName = data['fullName']
		order.email = data['email']
		order.phone = data['phone']
		order.deliveryType = delivery_name
		order.paymentType = data['paymentType']
		order.totalCost = order_cost
		order.city = data['city']
		order.address = data['address']
		order.save()

		return Response(data={'orderId': order.pk}, status=status.HTTP_200_OK)


class PaymentView(APIView):
	"""
	Оплата заказа.
	"""
	permission_classes = [IsAuthenticated]

	def post(self, request: Request, pk) -> Response:
		"""
		Ввод данных для оплаты заказа.

		:param request: Запрос
		:param pk: Идентификатор заказа
		:return: response_data
		"""
		data = json.loads(request.body)
		number = data['number']
		month = data['month']
		year = data['year']
		code = data['code']
		name = data['name']
		response_data = {}

		# Проверка чисел на кол-во цифр и наличии букв.
		if len(number) == 8 and number.isdigit():
			response_data['number'] = number
		if len(month) == 2 and month.isdigit():
			response_data['month'] = month
		if len(year) == 4 and year.isdigit():
			response_data['year'] = year
		if len(code) == 3 and code.isdigit():
			response_data['code'] = code

		# Проверка наличия 2-х слов в имени.
		name = name.strip()
		count_words = len(name.split(' '))

		if count_words == 2:
			full_name = name.replace(' ', '')
			if full_name.isalpha():
				response_data['name'] = name

		# Если все 5 полей есть в ответе, то успешный вывод.
		if len(response_data.keys()) == 5:
			order = Order.objects.get(pk=pk, archived=False)

			# Если номер карты заканчивается на 0, то статус заказа оплачен.
			if number[len(number) - 1] == '0':
				order.status = 'paid'

				# Уменьшение кол-ва товара и кол-ва проданных в каталоге при успешной оплате
				products_order = (
					ProductOrder.objects
					.select_related('productId')
					.filter(orderId=pk)
				)

				for item in products_order:
					product = item.productId
					product.count -= item.count
					product.salesCount += item.count
					product.save()
			else:
				order.status = 'payment error'
			order.save()

			return Response(data=response_data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
