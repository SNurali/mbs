from django.db.models import Avg
from datetime import datetime

from .models import Tag, Product, Review, Specification

from rest_framework import serializers


class ImageProductSerializer(serializers.ModelSerializer):
	"""
	Сериализация изображений для товара.
	"""
	def to_representation(self, instance):
		"""
		Вывод пути src и название alt изображения.

		:param instance: Изображение
		:return: src and alt
		"""
		return {
			'src': instance.image.url,
			'alt': instance.image.name
		}


class SpecificationSerializer(serializers.ModelSerializer):
	"""
	Сериализация спецификаций к товару.
	"""
	class Meta:
		"""
		Модель спецификации с полями.
		"""
		model = Specification
		fields = 'name', 'value'


class TagsSerializer(serializers.ModelSerializer):
	"""
	Сериализация списка тегов.
	"""
	class Meta:
		"""
		Модель тегов с полями.
		"""
		model = Tag
		fields = 'id', 'name'


class ReviewSerializer(serializers.ModelSerializer):
	"""
	Сериализация отзывов к товарам.
	"""
	date = serializers.SerializerMethodField()

	class Meta:
		"""
		Модель отзывов с полями.
		"""
		model = Review
		fields = 'author', 'email', 'text', 'rate', 'date'

	def get_date(self, obj):
		return obj.date.strftime('%Y-%m-%d %H:%M')


class ProductSerializer(serializers.ModelSerializer):
	"""
	Сериализация товаров.
	"""
	images = ImageProductSerializer(many=True)
	tags = TagsSerializer(many=True)
	specifications = SpecificationSerializer(many=True)
	reviews = ReviewSerializer(many=True)
	price = serializers.SerializerMethodField()
	rating = serializers.SerializerMethodField()

	class Meta:
		"""
		Модель товаров с полями.
		"""
		model = Product
		fields = (
			'id',
			'category',
			'price',
			'salePrice',
			'count',
			'date',
			'title',
			'description',
			'fullDescription',
			'freeDelivery',
			'images',
			'tags',
			'reviews',
			'specifications',
			'rating',
		)

	def get_price(self, obj):
		"""
		Изменение цены товара, если указана цена по акции.

		:param obj: Товар
		:return: obj.price or obj.salePrice
		"""
		current_date = datetime.now().date()
		if obj.salePrice is not None and (obj.dateFrom <= current_date <= obj.dateTo):
			return obj.salePrice
		else:
			return obj.price

	def get_rating(self, obj):
		"""
		Рейтинг товара на основе отзывов к товару.

		:param obj: Товар
		:return: avg_rating['rate__avg'] or 0
		"""
		if obj.reviews.count():
			avg_rating = obj.reviews.aggregate(Avg('rate'))
			return round(avg_rating['rate__avg'], 2)
		else:
			return 0


