from .models import Tag, Product, Review

from rest_framework import serializers


class ImageProductSerializer(serializers.ModelSerializer):
	"""
	Сериализация изображений для товара.
	"""
	def to_representation(self, instance):
		return {'src': instance.image.url, 'alt': instance.image.name}


class TagProductSerializer(serializers.ModelSerializer):
	"""
	Сериализация тэгов для товаров.
	"""
	def to_representation(self, instance):
		return {'name': instance.name}


class SpecificationSerializer(serializers.ModelSerializer):
	"""
	Сериализация спецификаций к товару.
	"""
	def to_representation(self, instance):
		return {'name': instance.name, 'value': instance.value}


class ReviewProductSerializer(serializers.ModelSerializer):
	"""
	Сериализация отзывов к товару.
	"""
	def to_representation(self, instance):
		return {
			"author": instance.author,
			"email": instance.email,
			"text": instance.text,
			"rate": instance.rate,
			"date": instance.date
		}


class TagsSerializer(serializers.ModelSerializer):
	"""
	Сериализация списка тегов.
	"""

	class Meta:
		model = Tag
		fields = 'id', 'name'


class ProductSerializer(serializers.ModelSerializer):
	"""
	Сериализация товаров.
	"""
	images = ImageProductSerializer(many=True)
	tags = TagProductSerializer(many=True)
	specifications = SpecificationSerializer(many=True)
	reviews = ReviewProductSerializer(many=True)

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
			'fullDescription',
			'freeDelivery',
			'images',
			'tags',
			'reviews',
			'specifications',
			'rating',
		)

class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = 'author', 'email', 'text', 'rate', 'date'
