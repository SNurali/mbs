from django.db import models
from django.core.validators import MinValueValidator

from profileapp.models import Profile
from productapp.models import Product


class Order(models.Model):
	"""
	Модель заказа.
	"""
	class Meta:
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'

	createdAt = models.DateTimeField(auto_now_add=True)
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
	fullName = models.CharField(null=True, blank=True, max_length=100)
	email = models.EmailField(null=True, blank=True, max_length=50)
	phone = models.PositiveIntegerField(null=True, blank=True)
	deliveryType = models.CharField(max_length=30)
	paymentType = models.CharField(max_length=30, default='online')
	totalCost = models.FloatField()
	status = models.CharField(max_length=30, default='accepted')
	city = models.CharField(max_length=30, blank=True)
	address = models.TextField(max_length=100, blank=True)
	archived = models.BooleanField(default=False)

	def __str__(self):
		return f'№{self.id}'

	def delete(self) -> None:
		"""
		При удалении заказ архивируется.

		:return: None
		"""
		self.archived = True
		self.save()


class ProductOrder(models.Model):
	"""
	Модель связи товара к заказу с кол-вом для заказа.
	"""
	class Meta:
		verbose_name = 'Товар заказа'
		verbose_name_plural = 'Товары заказов'

	orderId = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
	productId = models.ForeignKey(Product, on_delete=models.CASCADE)
	count = models.PositiveIntegerField(validators=[MinValueValidator(1)])

	def __str__(self):
		return f'Товар {self.productId} к заказу {self.orderId}'


class Delivery(models.Model):
	"""
	Модель доставок.
	"""
	class Meta:
		verbose_name = 'Доставка'
		verbose_name_plural = 'Доставки'

	name = models.CharField(max_length=30)
	maxCost = models.PositiveIntegerField(null=True, blank=True)
	deliveryPrice = models.PositiveIntegerField()

	def __str__(self):
		return f'{self.name}'
