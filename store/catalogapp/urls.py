from django.urls import path

from .views import CategoryView, CatalogView, ProductsPopularView, ProductsLimitedView, SaleView

app_name = 'catalogapp'

urlpatterns = [
	path('categories', CategoryView.as_view(), name='categories'),
	path('catalog', CatalogView.as_view(), name='catalog'),
	path('products/popular', ProductsPopularView.as_view(), name='products_popular'),
	path('products/limited', ProductsLimitedView.as_view(), name='products_limited'),
	path('sales', SaleView.as_view(), name='sale'),
	path('banners', ProductsPopularView.as_view(), name='banners'),
]
