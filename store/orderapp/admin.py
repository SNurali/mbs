from django.contrib import admin

from .models import Delivery, Order, ProductOrder
from .forms import OrderAdminValidateForm, ProductOrderAdminValidatorForm


class ProductOrderInline(admin.TabularInline):
	"""
	Таблица товаров с кол-вом к заказу.
	"""
	model = ProductOrder


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
	"""
	Модель доставок для админки.
	Сортировка по названию и идентификатору.
	Поиск по названию, максимальной цене и цене доставки.
	"""
	list_display = 'id', 'name', 'maxCost', 'deliveryPrice'
	ordering = 'name', 'id'
	search_fields = 'name', 'maxCost', 'deliveryPrice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	"""
	Модель заказа для админки.
	Сортировка по дате созданию (по убыванию) и идентификатору.
	Поиск по полям город, адрес, стоимость.
	Только для чтения поле стоимости.
	Таблица ProductOrder для добавления товаров к заказу.
	"""
	list_display = 'id', 'profile', 'totalCost', 'city', 'address_short', 'status'
	list_filter = 'deliveryType', 'paymentType'
	form = OrderAdminValidateForm
	ordering = '-createdAt', 'id'
	search_fields = 'city', 'address', 'totalCost'
	readonly_fields = 'totalCost',
	inlines = [ProductOrderInline]
	fieldsets = [
		(None, {
			'fields': ('status', 'paymentType', 'totalCost')
		}),
		('Заказчик', {
			'fields': ('profile', 'fullName', 'email', 'phone'),
		}),
		('Доставка', {
			'fields': ('deliveryType', 'city', 'address'),
		}),
		('Дополнительные опции', {
			'fields': ('archived', ),
			'classes': ('collapse', ),
			'description':
				'Для заказов используется Soft Delete (мягкое удаление). '
				'При активном поле archived заказ будет сохранен в архиве.',
		})
	]

	def address_short(self, obj):
		"""
		Ограничение размера поля address до 30 символов.

		:param obj: Заказ
		:return: obj.address
		"""
		count_letter = 30
		if obj.address:
			if len(obj.address) <= count_letter:
				return obj.address
			return obj.address[:count_letter]


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
	"""
	Модель товара в заказе для админки.
	Сортировка по названию продукта и идентификатору.
	Поиск по названию товара и идентификатору заказа.
	"""
	list_display = 'id', 'orderId', 'productId', 'count'
	form = ProductOrderAdminValidatorForm
	ordering = 'productId__title', 'id'
	search_fields = 'productId__title', 'orderId__id'
