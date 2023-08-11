from django.urls import path

from .views import ProductView, TagsView, ProductReviewView


urlpatterns = [
	path('product/<int:pk>', ProductView.as_view(), name='product'),
	path('product/<int:pk>/reviews', ProductReviewView.as_view(), name='product_review'),
	path('tags', TagsView.as_view(), name='tags'),
]