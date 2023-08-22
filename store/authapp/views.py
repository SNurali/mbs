import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from profileapp.models import Profile

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


class SignInViewClass(APIView):
	"""
	Авторизация пользователя по логину и паролю.
	"""
	def post(self, request: Request) -> Response:
		data = json.loads(request.body)
		username = data['username']
		password = data['password']

		# Проверка учетной записи
		user = authenticate(request, username=username, password=password)

		# Если учетная запись есть и профиль не в архиве, то авторизация, иначе ошибка 401
		if user and user.profile.archived is not True:
			login(request, user)
		else:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		return Response(status=status.HTTP_200_OK)


class SignOutViewClass(APIView):
	"""
	Выход из учетной записи.
	"""
	def post(self, request: Request) -> Response:
		"""
		Выход из учетной записи.

		:param request: Запрос
		:return: Response
		"""
		logout(request)

		return Response(status=status.HTTP_200_OK)


class SignUPViewClass(APIView):
	"""
	Регистрация пользователя.
	"""
	def post(self, request: Request) -> Response:
		data = json.loads(request.body)
		username = data['username']
		password = data['password']
		name = data['name']

		# Создание нового пользователя.
		register = User.objects.create_user(username=username, password=password, first_name=name)

		# Если пользователь успешно создан, то обновление профиля и авторизация.
		if register:
			# Обновление имени в профиле пользователя.
			profile = Profile.objects.get(user=register)
			profile.fullName = name
			profile.save()
			# Авторизация.
			user = authenticate(request, username=username, password=password)
			login(request, user)

			return Response(status=status.HTTP_200_OK)

		return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
