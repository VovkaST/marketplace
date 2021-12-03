from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppLoaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_import'
    verbose_name = _('Loader')
