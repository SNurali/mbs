import json

from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage

from .models import Profile
from .serializers import ProfileSerializer

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class ProfileView(APIView):
	"""
	Профиль авторизованного пользователя и изменение основных данных.
	"""
	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:
		"""
		Вывод данных профиля

		:param request: запрос
		:return: serialized.data
		"""
		profile = (
			Profile.objects
			.select_related('user')
			.get(user=request.user, archived=False)
		)
		serialized = ProfileSerializer(profile)

		return Response(data=serialized.data, status=status.HTTP_200_OK)

	def post(self, request: Request):
		"""
		Изменение основных данных профиля (имя, email, телефон).

		:param request: Получаемые данные
		:return: serialized.data
		"""
		data = json.loads(request.body)
		full_name = data['fullName']
		email = data['email']
		phone = data['phone']
		profile = Profile.objects.get(user=request.user, archived=False)

		# Проверка на существование профилей с введенными данными, исключая собственный.
		check_email = Profile.objects.filter(email=email, archived=False).exclude(user=request.user)
		check_phone = Profile.objects.filter(phone=phone, archived=False).exclude(user=request.user)

		# Если имя или email не заполнены либо email и телефон не уникальны, то ошибка.
		if not full_name or not email:
			raise ValueError('Full name or email is not filled')
		elif check_email:
			raise ValueError('Email already in use')
		elif check_phone:
			raise ValueError('Phone already in use')

		# Изменение данных профиля в БД.
		profile.fullName = full_name
		profile.email = email
		profile.phone = phone
		profile.save()

		serialized = ProfileSerializer(profile)

		return Response(data=serialized.data, status=status.HTTP_200_OK)


class ChangeAvatarView(APIView):
	"""
	Смена аватара в профиле пользователя.
	"""
	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> Response:
		"""
		Загрузка нового аватара профиля.

		:param request: Изображение
		:return: None
		"""
		profile = (
			Profile.objects
			.select_related('user')
			.get(user=request.user, archived=False)
		)

		# Сохранение аватара в uploads/.
		avatar = request.FILES['avatar']

		# Максимальный размер изображения не более 2 Мб.
		if avatar.size > (2 * 1024 * 1024):
			raise FileNotFoundError('Image avatar size is large 2Mb')

		fs = FileSystemStorage(
			location=f'uploads/profile/user_{profile.user.pk}/avatar/'
		)
		filename = fs.save(avatar.name, avatar)

		# Обновление пути к изображению в профиле.
		profile.avatar = f'profile/user_{profile.user.pk}/avatar/' + filename
		profile.save()

		return Response(status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
	"""
	Смена пароля в профиле пользователя.
	"""
	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> Response:
		"""
		Смена старого пароля на новый, после этого авторизация с новым паролем.

		:param request: Введённые данные
		:return: None
		"""
		data = json.loads(request.body)
		current_password = data['currentPassword']
		new_password = data['newPassword']

		user = request.user

		# Проверка правильно ли введен текущий пароль.
		if not user.check_password(current_password):
			raise ValueError('Current password is wrong')

		# Установка нового пароля.
		user.set_password(new_password)
		user.save()

		# Авторизация пользователя после смены пароля.
		user = authenticate(request, username=user.username, password=new_password)
		login(request, user)

		return Response(status=status.HTTP_200_OK)


