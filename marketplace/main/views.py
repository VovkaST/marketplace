from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from django.views.generic.base import TemplateView
from services.cache_settings import cache_settings

from services.main_page import get_banners
from services.cache_settings import MAIN_BANNERS_CACHE


class BannerMixin(ContextMixin):
    """Выбор баннеров и занесение их в context"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banners = get_banners()
        context["banners"] = banners
        context["banners_cache_value"] = MAIN_BANNERS_CACHE
        return context


class CacheSettingsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'cache_settings': cache_settings})
        return context


class MarketMain(TemplateView, BannerMixin):
    """Представление главной страницы магазина"""

    template_name = "main/index.html"

