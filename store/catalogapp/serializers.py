from productapp.serializers import ProductSerializer
from datetime import datetime

from .models import Category

from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
	"""
	Сериализация изображения категории.
	"""
	def to_representation(self, instance):
		"""
		Вывод пути и названия изображения.

		:param instance: Изображение
		:return: {'src': instance.url, 'alt': instance.name}
		"""
		return {'src': instance.url, 'alt': instance.name}


class CategorySerializer(serializers.ModelSerializer):
	"""
	Сериализация списка категорий.
	"""
	image = ImageSerializer()
	subcategories = serializers.SerializerMethodField()

	class Meta:
		"""
		Список полей для вывода категории.
		"""
		model = Category
		fields = 'id', 'title', 'image', 'subcategories'

	def get_subcategories(self, obj):
		"""
		Рекурсивная сериализация списка подкатегорий.

		:param obj: Категория
		:return: Список подкатегорий
		"""
		if obj.parent is None:
			# Если текущая категория без родителя, то выводятся связанные подкатегории.
			serialized = CategorySerializer(obj.subcategories, many=True)
			return serialized.data
		else:
			return []


class CatalogSerializer(ProductSerializer):
	"""
	Сериализация всех товаров в каталоге.
	Родительская сериализация ProductSerializer.
	"""
	reviews = serializers.SerializerMethodField()

	class Meta(ProductSerializer.Meta):
		"""
		Список полей для вывода товара.
		Дочерняя метамодель от ProductSerializer.
		"""
		fields = (
			'id',
			'category',
			'price',
			'count',
			'date',
			'title',
			'description',
			'freeDelivery',
			'images',
			'tags',
			'reviews',
			'rating'
		)

	def get_reviews(self, obj):
		"""
		Вывод кол-ва отзывав к товару.

		:param obj: Товар
		:return: obj.reviews.count()
		"""
		return obj.reviews.count()


class CatalogSaleSerializer(ProductSerializer):
	"""
	Сериализация товаров с ценой по скидке.
	Родительская сериализация ProductSerializer.
	"""
	date_format = '%m-%d'
	dateFrom = serializers.DateField(format=date_format)
	dateTo = serializers.DateField(format=date_format)
	price = serializers.SerializerMethodField()

	class Meta(ProductSerializer.Meta):
		"""
		Список полей для вывода товара.
		Дочерняя метамодель от ProductSerializer.
		"""
		fields = (
			'id',
			'price',
			'salePrice',
			'dateFrom',
			'dateTo',
			'title',
			'images',
		)

	def get_price(self, obj):
		"""
		Вывод реальной цены товара без акции.

		:param obj: Товар
		:return: obj.price
		"""
		return obj.price

