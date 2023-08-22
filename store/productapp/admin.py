from django.contrib import admin

from .models import Product, ProductImage, Tag, Review, Specification

class ProductImageTabular(admin.TabularInline):
	"""
	Таблица изображений для товара.
	"""
	model = ProductImage


class SpecificationTabular(admin.TabularInline):
	"""
	Таблица спецификаций для товаров.
	"""
	model = Specification


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	"""
	Модель товара в админке.
	Сортировка по названию товара и идентификатору.
	Поиск по названию, описанию и названию категории.
	Дополнительно выводится таблицы ProductImage, Specification.
	Только для чтения поля рейтинг и кол-во продаж.
	"""
	list_display = 'id', 'title', 'category', 'price', 'salePrice', 'description_short'
	list_filter = 'tags',
	ordering = 'title', 'id',
	search_fields = 'title', 'description', 'category__title'
	inlines = [ProductImageTabular, SpecificationTabular]
	readonly_fields = 'rating', 'salesCount', 'date'
	fieldsets = [
		(None, {
			'fields': ('title', 'description', 'fullDescription', 'freeDelivery', 'category'),
		}),
		('Информация', {
			'fields': ('count', 'salesCount', 'rating', 'date'),
		}),
		('Цена', {
			'fields': ('price',),
		}),
		('Цена по акции', {
			'fields': ('salePrice', 'dateFrom', 'dateTo'),
			'classes': ('collapse',),
			'description':
				'Если не указан salePrice, то цена товара стандартная от поля price. '
				'Поле salePrice предназначен для акционной цены товара в период от dateFrom до dateTo.',
		}),
		('Дополнительные опции', {
			'fields': ('archived',),
			'classes': ('collapse',),
			'description':
				'Для товаров используется Soft Delete (мягкое удаление). '
				'При активном поле archived товары будут сохранены в архиве.',
		}),
		('Теги', {
			'fields': ('tags',),
		}),
	]

	def description_short(self, obj: Product) -> str:
		"""
		Ограничение вывода описания товара до 30 символов.

		:param obj: Товар
		:return: obj.description
		"""
		count_letter = 30
		if obj.description:
			if len(obj.description) <= count_letter:
				return obj.description
			return obj.description[:count_letter] + '...'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
	"""
	Модель изображения к товару в админке.
	Сортировка по названию товара и идентификатору.
	Поиск по названию товара.
	"""
	list_display = 'id', 'product', 'image'
	ordering = 'product', 'id'
	search_fields = 'product__title',


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	"""
	Модель тэга в админке.
	Сортировка по имени тэга и второстепенно по идентификатору.
	Поиск по названию тэга.
	"""
	list_display = 'id', 'name'
	ordering = 'name', 'id'
	search_fields = 'name',


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	"""
	Модель отзыва к товару.
	Сортировка по названию товара, рейтингу (по убыванию) и идентификатору.
	Поиск по названию товара и автору отзыва.
	"""
	list_display = 'id', 'product', 'text_short', 'rate', 'author'
	ordering = 'product', '-rate', 'id'
	search_fields = 'product__title', 'author'

	def text_short(self, obj: Review):
		count_letter = 30
		if obj.text:
			if len(obj.text) <= count_letter:
				return obj.text
			else:
				return obj.text[:count_letter]


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
	"""
	Модель спецификации к товару.
	Сортировка по названию товара, названию спецификации и идентификатору.
	Поиск по названию товара и названию спецификации.
	"""
	list_display = 'id', 'product', 'name', 'value'
	ordering = 'product', 'name', 'id'
	search_fields = 'product__title', 'name'
