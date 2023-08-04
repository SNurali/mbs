from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


class SignInViewClass(APIView):
	def post(self, request):
		if request.user.is_authenticated:
			return redirect('/')

		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			return redirect('/admin/')

		return render(request, 'frontend/signIn.html')
