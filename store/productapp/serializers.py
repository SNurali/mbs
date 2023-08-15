from statistics import mean

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
		return {
			'id': instance.pk,
			'name': instance.name
		}


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
	price = serializers.SerializerMethodField()
	rating = serializers.SerializerMethodField()

	class Meta:
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
		product = Product.objects.get(pk=obj.pk)
		if product.salePrice is None:
			return product.price
		else:
			return product.salePrice

	def get_rating(self, obj):
		reviews = Review.objects.filter(product=obj.pk)
		if reviews:
			reviews_rate = [review.rate for review in reviews]
			average_rating = round(mean(reviews_rate), 2)

			return average_rating
		else:
			return 0


class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = 'author', 'email', 'text', 'rate', 'date'
