from django import forms

from .models import Order, ProductOrder


class OrderAdminValidateForm(forms.ModelForm):
	"""
	Валидация заказа в админке.
	"""
	model = Order
	fields = 'fullName',

	def clean_fullName(self):
		"""
		Валидация поля ФИО.

		:return: full_name
		"""
		full_name = self.cleaned_data['fullName']

		# Если есть цифра в ФИО, то исключение.
		if not full_name.replace(' ', '').isalpha():
			raise forms.ValidationError('ФИО не может содержать цифры.')

		return full_name


class ProductOrderAdminValidatorForm(forms.ModelForm):
	"""
	Валидация формы продукт к заказу в админке.
	"""
	model = ProductOrder
	fields = 'orderId', 'productId'

	def clean(self):
		"""
		Валидация полей заказ и товар.

		:return: self.cleaned_data
		"""
		order = self.cleaned_data['orderId']
		product = self.cleaned_data['productId']

		# Проверка привязан ли уже такой товар к заказу.
		product_order = ProductOrder.objects.filter(orderId=order.pk, productId=product.pk)
		if product_order:
			raise forms.ValidationError(f'К заказу {order.pk} уже был добавлен товар {product.title}.')

		return self.cleaned_data
