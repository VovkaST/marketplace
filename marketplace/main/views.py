from django.views.generic.base import ContextMixin, TemplateView

from services.main_page import get_banners, get_categories
from services.cache_settings import cache_settings


class CacheSettingsMixin(ContextMixin):
    """Миксин для настроек кэша"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'cache_settings': cache_settings})
        return context


class BannerMixin(ContextMixin):
    """Выбор баннеров и занесение их в context"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banners = get_banners()
        context["banners"] = banners
        return context


class CategoryMixin(ContextMixin):
    """Получение всех категорий для вывода на главную страницу"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = get_categories()
        context['categories'] = categories
        return context


class MarketMain(TemplateView, BannerMixin, CategoryMixin, CacheSettingsMixin):
    """Представление главной страницы магазина"""

    template_name = "main/index.html"
