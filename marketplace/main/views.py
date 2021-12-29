from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin, TemplateView

from services.cache_settings import cache_settings
from services.main_page import get_banners, get_categories, get_top_goods


class PageInfoMixin(ContextMixin):
    """Миксин добавления названия страницы"""

    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': self.page_title
        })
        return context


class CacheSettingsMixin(ContextMixin):
    """Миксин для настроек кэша"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"cache_settings": cache_settings})
        return context


class BannerMixin(CacheSettingsMixin, ContextMixin):
    """Выбор баннеров и занесение их в context"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banners = get_banners()
        context["banners"] = banners
        return context


class CategoryMixin(CacheSettingsMixin, ContextMixin):
    """Получение всех категорий для вывода на главную страницу"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = get_categories()
        context["categories"] = categories
        return context


class TopGoodsMixin(ContextMixin):
    """Миксин топ-товаров"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_goods"] = get_top_goods()
        return context


class MarketMain(BannerMixin, CategoryMixin, TopGoodsMixin, TemplateView):
    """Представление главной страницы магазина"""

    template_name = "main/index.html"


class ContactsMain(PageInfoMixin, CategoryMixin, TemplateView):
    """Представление страницы контактов магазина"""

    template_name = "main/contacts.html"
    page_title = _('Contacts')


class AboutUsView(PageInfoMixin, CategoryMixin, TopGoodsMixin, TemplateView):
    """Представление страницы информации о магазине"""

    template_name = "main/about.html"
    page_title = _('About us')
