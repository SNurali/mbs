from .models import Profile

from rest_framework import serializers


class AvatarProfileSerializer(serializers.Serializer):
	"""
	Сериализация аватара профиля. Вывод пути изображения и названия.
	"""
	def to_representation(self, instance):
		"""
		Сериализация аватара с src и alt.

		:param instance: аватар
		:return: None or {'src': instance.url, 'alt': instance.name}
		"""
		if not instance:
			return None
		return {'src': instance.url, 'alt': instance.name}


class ProfileSerializer(serializers.ModelSerializer):
	"""
	Сериализация данных профиля.
	"""
	avatar = AvatarProfileSerializer()

	class Meta:
		"""
		Поля вывода профиля.
		"""
		model = Profile
		fields = (
			'fullName',
			'email',
			'phone',
			'avatar'
		)
