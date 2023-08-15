from productapp.serializers import ProductSerializer
from .models import Category
from productapp.models import Review, Product

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


class CatalogSerializer(ProductSerializer):
	reviews = serializers.SerializerMethodField()

	class Meta(ProductSerializer.Meta):
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
		return len(Review.objects.filter(product=obj))


class ProductSaleDateSerializer(serializers.Serializer):
	def to_representation(self, instance):
		return instance.strftime('%m-%d')


class ProductSaleSerializer(ProductSerializer):
	"""
	Сериализация товаров по скидке (распродажа).
	"""
	dateFrom = ProductSaleDateSerializer()
	dateTo = ProductSaleDateSerializer()
	price = serializers.SerializerMethodField()

	class Meta(ProductSerializer.Meta):
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
		product = Product.objects.get(pk=obj.pk)
		return product.price
