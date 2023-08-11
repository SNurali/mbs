from django.urls import path

from .views import CategoryView, CatalogView

app_name = 'catalogapp'

urlpatterns = [
	path('categories', CategoryView.as_view(), name='categories'),
	path('catalog', CatalogView.as_view(), name='catalog'),
]