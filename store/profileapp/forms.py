from django import forms

from .models import Profile


class ProfileAdminValidateForm(forms.ModelForm):
	"""
	Валидация формы профиля в админке.
	"""
	class Meta:
		model = Profile
		fields = '__all__'

	def clean_fullName(self):
		"""
		Валидация поля ФИО профиля.

		:return: full_name
		"""
		full_name = self.cleaned_data['fullName']

		if full_name is None:
			raise forms.ValidationError('Поле обязательное к заполнению.')
		elif not full_name.replace(' ', '').isalpha():
			raise forms.ValidationError('ФИО пользователя не может содержать цифры.')

		return full_name

	def clean_email(self):
		"""
		Валидация поля email в профиле.

		:return: email
		"""
		email = self.cleaned_data['email']

		profile = Profile.objects.filter(email=email)

		if email is None:
			raise forms.ValidationError('Поле обязательное к заполнению.')
		elif profile:
			raise forms.ValidationError('Профиль с таким email уже существует.')

		return email

	def clean_phone(self):
		"""
		Валидация поля номер телефона в профиле.

		:return: phone
		"""
		phone = self.cleaned_data['phone']

		profile = Profile.objects.filter(phone=phone)

		if phone is None:
			raise forms.ValidationError('Поле обязательное к заполнению.')
		elif len(str(phone)) != 11:
			raise forms.ValidationError('Телефон должен состоять из 11 цифр.')
		elif profile:
			raise forms.ValidationError('Профиль с таким номером телефона уже существует.')

		return phone

	def clean_avatar(self):
		"""
		Валидация поля аватар в профиле.

		:return: avatar
		"""
		avatar = self.cleaned_data['avatar']

		# Проверка размера аватара (не больше 2 Мб).
		if avatar and avatar.size > (2 * 1024 * 1024):
			raise forms.ValidationError('Размер аватара не может превышать 2 Мб.')

		return avatar
