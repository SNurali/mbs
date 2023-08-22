from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def profile_avatar_directory_path(instance: 'Profile', filename: str) -> str:
	"""
	Загрузка аватара в определенную директорию.

	:param instance: профиль
	:param filename: название изображения
	:return: 'profile/user_{id}/avatar/{filename}'
	"""
	return 'profile/user_{id}/avatar/{filename}'.format(
		id=instance.user.id,
		filename=filename
	)


class Profile(models.Model):
	"""
	Профиль пользователя.
	"""
	class Meta:
		verbose_name = 'Профиль'
		verbose_name_plural = 'Профили'

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	fullName = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=50, null=True, blank=True)
	phone = models.PositiveIntegerField(null=True, blank=True)
	avatar = models.ImageField(null=True, blank=True, upload_to=profile_avatar_directory_path)
	archived = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.user.username}'

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs) -> None:
		"""
		Автоматическое создание профиля при добавлении пользователя.

		:param instance: Пользователь
		:param created: Создан ли пользователь
		:param kwargs: Позиционные аргументы
		:return: None
		"""
		if created:
			Profile.objects.create(user=instance)

	def delete(self) -> None:
		"""
		При удалении профиль архивируется.

		:return:
		"""
		self.archived = True
		self.save()