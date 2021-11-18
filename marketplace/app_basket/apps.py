from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppBasketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_basket'
    verbose_name = _('Basket')
