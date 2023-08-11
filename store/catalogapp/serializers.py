from itertools import count

from .models import Category
from productapp.models import Review
from productapp.models import Product

from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
	def to_representation(self, instance):
		return {'src': instance.url, 'alt': instance.name}


class CategorySerializer(serializers.ModelSerializer):
	"""
	Сериализация списка категорий.
	"""
	image = ImageSerializer(many=False)
	subcategories = serializers.SerializerMethodField()

	class Meta:
		model = Category
		fields = 'id', 'title', 'image', 'subcategories'

	def get_subcategories(self, obj):
		"""
		Рекурсивная сериализация списка подкатегорий.
		:param obj: (object) родительская категория
		:return: (list) список из подкатегорий
		"""
		if obj.parent is None:
			return [CategorySerializer(i_cat).data for i_cat in Category.objects.filter(parent=obj)]
		else:
			return []


class ImageItemSerializer(serializers.ModelSerializer):
	"""
	Сериализация изображений для товара.
	"""
	def to_representation(self, instance):
		return {'src': instance.image.url, 'alt': instance.image.name}


class TagItemSerializer(serializers.ModelSerializer):
	"""
	Сериализация тэгов для товаров.
	"""
	def to_representation(self, instance):
		return {'id': instance.pk, 'name': instance.name}


class CatalogSerializer(serializers.ModelSerializer):
	images = ImageItemSerializer(many=True)
	tags = TagItemSerializer(many=True)
	reviews = serializers.SerializerMethodField()

	class Meta:
		model = Product
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
			'rating',
		)

	def get_reviews(self, obj):
		return len(Review.objects.filter(product=obj))
