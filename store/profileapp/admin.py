from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile
from .forms import ProfileAdminValidateForm


class ProfileInline(admin.TabularInline):
	"""
	Таблица с профилем к пользователю для админки.
	"""
	model = Profile


class CustomUserAdmin(UserAdmin):
	"""
	Добавление таблицы с профилем к модели пользователей для админки.
	"""
	inlines = [ProfileInline]


# Отмена регистрации пользователей в админке и добавление с кастомизацией.
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	"""
	Модель профиля в админке.
	Сортировка по полям пользователь и идентификатор.
	Поиск по полям никнейм пользователя, ФИО, эл. почта, телефон.
	"""
	form = ProfileAdminValidateForm
	list_display = 'id', 'user', 'fullName', 'email', 'phone'
	ordering = 'user', 'id'
	search_fields = 'user__username', 'fullName', 'email', 'phone'
	fieldsets = [
		(None, {
			'fields': ('user', 'fullName', 'email', 'phone', 'avatar'),
		}),
		('Дополнительные опции', {
			'fields': ('archived', ),
			'classes': ('collapse', ),
			'description':
				'Для товаров используется Soft Delete (мягкое удаление). '
				'При активном поле archived товары будут сохранены в архиве.',
		})
	]

