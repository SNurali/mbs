from django.contrib.auth.models import User
from django.db import models

from store.settings import MEDIA_URL


def profile_avatar_directory_path(instance: 'Profile', filename: str) -> str:
	return 'profile/user_{id}/avatar/{filename}'.format(
		id=instance.user.id,
		filename=filename
	)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	fullName = models.CharField(max_length=100, null=True, blank=True)
	email = models.EmailField(max_length=50, null=True, blank=True)
	phone = models.PositiveIntegerField(null=True, blank=True)
	avatar = models.ImageField(null=True, blank=True, upload_to=profile_avatar_directory_path)

	def __str__(self):
		return f'/{MEDIA_URL}profile/user_{self.user.pk}/avatar/{self.avatar}'

