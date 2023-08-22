from django.db import models


def category_image_upload_path(instance, filename) -> str:
	"""
	Определение пути изображения для категории товаров.

	:param instance: Категория
	:param filename: Имя файла
	:return: 'categories/category_{name}/{filename}'
	"""
	return 'categories/category_{name}/{filename}'.format(
		name=instance.title.replace(' ', '_'),
		filename=filename
	)


class Category(models.Model):
	"""
	Модель категорий товаров.
	"""
	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	title = models.CharField(max_length=50, null=False)
	image = models.ImageField(upload_to=category_image_upload_path)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
	archived = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.title}'

	def delete(self) -> None:
		"""
		При удалении категория архивируется.

		:return: None
		"""
		self.archived = True
		self.save()
