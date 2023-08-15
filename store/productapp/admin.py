from django.contrib import admin

from .models import Product, ProductImage, Tag, Review, Specification


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = 'id', 'title',
	ordering = 'id',


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
	list_display = 'id', 'product', 'image'
	ordering = 'id',


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = 'id', 'name'
	ordering = 'id',


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = 'id', 'product', 'text', 'rate', 'author'
	ordering = 'id',


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
	list_display = 'id', 'product', 'name', 'value'
	ordering = 'id',
