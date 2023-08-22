from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	"""
	Модель категорий для админки.
	Сортировка по имени и идентификатору.
	Поиск по названию и названию родительской категории.
	"""
	list_display = 'id', 'title', 'parent', 'image'
	ordering = 'title', 'id'
	search_fields = 'title', 'parent__title'
	fieldsets = [
		(None, {
			'fields': ('title', 'parent', 'image'),
		}),
		('Дополнительные опции', {
			'fields': ('archived', ),
			'classes': ('collapse', ),
			'description':
				'Для удаления категории используется Soft Delete (мягкое удаление). '
				'При активном поле archived категория будет сохранена в архиве.'
		})
	]
