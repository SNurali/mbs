import json

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .models import Profile

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class ProfileView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:
		profile = Profile.objects.get(user=request.user)

		response = {
			'fullName': profile.fullName,
			'email': profile.email,
			'phone': profile.phone,
			'avatar': {
				'src': profile.__str__(),
				'alt': 'Image my profile',
			}
		}

		return Response(response)

	def post(self, request: Request):
		data = json.loads(request.body)
		profile = Profile.objects.get(user=request.user)
		profile.fullName = data['fullName']
		profile.email = data['email']
		profile.phone = data['phone']
		profile.save()

		response = {
			'fullName': profile.fullName,
			'email': profile.email,
			'phone': profile.phone,
			'avatar': {
				'src': profile.__str__(),
				'alt': 'Image my profile'
			}
		}

		return Response(data=response, status=status.HTTP_200_OK)


class ChangeAvatarView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> Response:
		profile = Profile.objects.get(user=request.user)
		avatar = request.FILES['avatar']
		fs = FileSystemStorage(
			location=f'uploads/profile/user_{profile.user.pk}/avatar/'
		)
		filename = fs.save(avatar.name, avatar)
		profile.avatar = filename
		profile.save()

		return Response(status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> Response:
		data = json.loads(request.body)
		user = User.objects.get(pk=request.user.pk)

		if user.check_password(data['currentPassword']):
			user.set_password(data['newPassword'])
			user.save()
		else:
			raise TypeError('Load failed')

		return Response(status=status.HTTP_200_OK)


