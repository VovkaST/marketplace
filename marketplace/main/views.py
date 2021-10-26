from django.shortcuts import render
from django.views.generic.base import View, ContextMixin

from services.cache_settings import cache_settings


class MarketMain(View):
    """Представление главной страницы магазина"""

    def get(self, request):
        return render(request, 'main/index.html')


class CacheSettingsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'cache_settings': cache_settings})
        return context
