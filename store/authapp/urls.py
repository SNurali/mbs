from django.urls import path

from .views import SignInViewClass, SignOutViewClass, SignUPViewClass

app_name = 'authapp'

urlpatterns = [
	path('sign-in', SignInViewClass.as_view(), name='sign-in'),
	path('sign-out', SignOutViewClass.as_view(), name='sign-out'),
	path('sign-up', SignUPViewClass.as_view(), name='sign-up'),
]
