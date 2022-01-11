from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppComparisonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_comparison'
    verbose_name = _('Goods comparison')
