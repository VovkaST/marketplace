from django.views.generic.base import ContextMixin, TemplateView

from services.main_page import *
from services.cache_settings import *


class BannerMixin(ContextMixin):
    """Выбор баннеров и занесение их в context"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banners = get_banners()
        context["banners"] = banners
        context["banners_cache_value"] = MAIN_BANNERS_CACHE
        return context


class CategoryMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = get_categories()
        context['categories'] = categories
        context['categories_cache_value'] = MAIN_CATEGORIES_CACHE
        return context


class MarketMain(TemplateView, BannerMixin):
    """Представление главной страницы магазина"""

    template_name = "main/index.html"
