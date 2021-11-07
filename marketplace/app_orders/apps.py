from django.apps import AppConfig
from django.utils.translation import gettext as _


class AppOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_orders'
    verbose_name = _('Orders')
