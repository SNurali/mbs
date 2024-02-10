from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('api/', include('rest_framework.urls')),
    path('api/', include('authapp.urls')),
    path('api/', include('profileapp.urls')),
    path('api/', include('catalogapp.urls')),
    path('api/', include('productapp.urls')),
    path('api/', include('basketapp.urls')),
	path('api/', include('orderapp.urls')),
]

# загрузка статики
if settings.DEBUG:
	urlpatterns.extend(
		static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
	)
