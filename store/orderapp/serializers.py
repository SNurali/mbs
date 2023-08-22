from .models import Order
from catalogapp.serializers import CatalogSerializer

from .models import ProductOrder
from productapp.models import Product

from rest_framework import serializers


class ProductOrderSerializer(serializers.Serializer):
	"""
	Сериализация товаров к заказу.
	"""
	def to_representation(self, instance):
		"""
		Сериализация товара привязанной к заказу с кол-вом для заказа.

		:param instance: Товар заказа
		:return: serialized.data
		"""
		instance.productId.count = instance.count
		serialized = CatalogSerializer(instance.productId)
		return serialized.data


class OrderSerializer(serializers.ModelSerializer):
	"""
	Сериализация заказа.
	"""
	products = ProductOrderSerializer(many=True)
	createdAt = serializers.SerializerMethodField()

	class Meta:
		"""
		Список полей для заказа.
		"""
		model = Order
		fields = (
			'id',
			'createdAt',
			'fullName',
			'email',
			'phone',
			'deliveryType',
			'paymentType',
			'totalCost',
			'status',
			'city',
			'address',
			'products',
		)

	def get_createdAt(self, obj):
		"""
		Изменение формата даты создания заказа.

		:param obj: Заказ
		:return: obj.createdAt.strftime('%Y-%m-%d %H:%M')
		"""
		return obj.createdAt.strftime('%Y-%m-%d %H:%M')
