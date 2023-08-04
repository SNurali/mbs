from django.urls import path

from .views import SignInViewClass

app_name = 'authapp'

urlpatterns = [
	path('sign-in', SignInViewClass.as_view(), name='sign-in'),
]
