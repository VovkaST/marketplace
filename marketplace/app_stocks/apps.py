from django.apps import AppConfig
from django.utils.translation import gettext as _


class AppStocksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_stocks'
    verbose_name = _('Stocks')
