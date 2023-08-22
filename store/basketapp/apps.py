from django.apps import AppConfig


class BasketappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basketapp'
    verbose_name = 'Корзина'
