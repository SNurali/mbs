from django.db import models

from catalogapp.models import Category


def product_image_upload_path(instance, filename):
	return 'products/product_{pk}/images/{filename}'.format(
		pk=instance.product.pk,
		filename=filename
	)


class Tag(models.Model):
	name = models.CharField(max_length=30, null=False)


class Product(models.Model):
	class Meta:
		ordering = 'id',

	price = models.FloatField()
	salePrice = models.FloatField(null=True)
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
	tags = models.ManyToManyField(Tag, related_name='product')


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to=product_image_upload_path)


class Review(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
	author = models.CharField(max_length=50)
	email = models.EmailField(max_length=50, null=True, blank=True)
	text = models.TextField(max_length=300, null=True, blank=True)
	rate = models.PositiveIntegerField(null=False)
	date = models.DateTimeField(auto_now_add=True)


class Specification(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
	name = models.CharField(max_length=20)
	value = models.CharField(max_length=20)
