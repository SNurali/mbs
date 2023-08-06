import json

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from profileapp.models import Profile

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView


class SignInViewClass(APIView):  # авторизация пользователя
	def post(self, request: Request) -> Response:
		data = json.loads(request.body)
		username = data['username']
		password = data['password']

		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
		else:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		return Response(status=status.HTTP_200_OK)


class SignOutViewClass(APIView): #выход
	def post(self, request: Request) -> Response:
		logout(request)
		return Response(status=status.HTTP_200_OK)


class SignUPViewClass(APIView):  # регистрация пользователя
	def post(self, request: Request) -> Response:
		data = json.loads(request.body)
		username = data['username']
		password = data['password']
		name = data['name']
		register = User.objects.create_user(username=username, password=password, first_name=name)

		if register:
			profile = Profile.objects.create(user=register, fullName=name)
			user = authenticate(request, username=username, password=password)
			login(request, user)
			return Response(status=status.HTTP_200_OK)

		return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
