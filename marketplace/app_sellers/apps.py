from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppSellersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_sellers'
    verbose_name = _('Sellers')
