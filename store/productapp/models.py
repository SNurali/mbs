from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from catalogapp.models import Category


def product_image_upload_path(instance, filename):
	"""
	Путь к изображениям товара.

	:param instance: Изображение
	:param filename: Название изображение
	:return: 'products/product_{pk}/images/{filename}'
	"""
	return 'products/product_{pk}/images/{filename}'.format(
		pk=instance.product.pk,
		filename=filename
	)


class Tag(models.Model):
	"""
	Модель тэгов.
	"""
	class Meta:
		verbose_name = 'Тэг'
		verbose_name_plural = 'Теги'

	name = models.CharField(max_length=30, null=False)

	def __str__(self):
		return f'{self.name}'


class Product(models.Model):
	"""
	Модель товара.
	"""
	class Meta:
		ordering = 'id',
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'

	price = models.FloatField(validators=[MinValueValidator(1)])
	salePrice = models.FloatField(null=True, blank=True)
	dateFrom = models.DateField(null=True, blank=True)
	dateTo = models.DateField(null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	count = models.PositiveIntegerField()
	date = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=30)
	description = models.TextField(max_length=100, null=True, blank=True)
	fullDescription = models.TextField(max_length=300, null=True, blank=True)
	freeDelivery = models.BooleanField(default=False)
	rating = models.FloatField(default=0)
	tags = models.ManyToManyField(Tag, blank=True, related_name='product')
	salesCount = models.PositiveIntegerField(default=0)
	archived = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.title}'

	def delete(self) -> None:
		"""
		При удалении товар помещается в архив.

		:return: None
		"""
		self.archived = True
		self.save()


class ProductImage(models.Model):
	"""
	Модель изображения к товару.
	"""
	class Meta:
		verbose_name = 'Изображение'
		verbose_name_plural = 'Изображения'

	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to=product_image_upload_path)

	def __str__(self):
		return f'Изображение к товару {self.product}'


class Review(models.Model):
	"""
	Модель отзыва к товару.
	"""
	class Meta:
		verbose_name = 'Отзыв'
		verbose_name_plural = 'Отзывы'

	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
	author = models.CharField(max_length=50, default='Без имени')
	email = models.EmailField(max_length=50, null=True, blank=True)
	text = models.TextField(max_length=300, null=True, blank=True)
	rate = models.PositiveIntegerField(null=False, validators=[MaxValueValidator(5)])
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'Отзыв к товару {self.product}'


class Specification(models.Model):
	"""
	Модель спецификации к товару.
	"""
	class Meta:
		verbose_name = 'Спецификация'
		verbose_name_plural = 'Спецификации'

	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
	name = models.CharField(max_length=20)
	value = models.CharField(max_length=20)

	def __str__(self):
		return f'{self.name}'
