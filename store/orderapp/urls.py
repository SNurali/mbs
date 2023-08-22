from django.urls import path
from .views import OrdersView, OrderView, PaymentView

app_name = 'orderapp'

urlpatterns = [
	path('orders', OrdersView.as_view(), name='orders'),
	path('order/<int:pk>', OrderView.as_view(), name='order'),
	path('payment/<int:pk>', PaymentView.as_view(), name='payment'),
]
