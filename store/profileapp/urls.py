from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import ProfileView, ChangeAvatarView, ChangePasswordView

app_name = 'profileapp'

urlpatterns = [
	path('profile/', ProfileView.as_view(), name='profile_get'),
	path('profile', ProfileView.as_view(), name='profile_post'),
	path('profile/avatar', ChangeAvatarView.as_view(), name='change_avatar'),
	path('profile/password', ChangePasswordView.as_view(), name='change_password'),
]