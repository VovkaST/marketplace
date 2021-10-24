from django.views.generic.base import ContextMixin, TemplateView

from marketplace.services.cache_settings import MAIN_BANNERS_CACHE
from marketplace.services.main_page import get_banners


class BannerMixin(ContextMixin):
    """Выбор баннеров и занесение их в context"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banners = get_banners()
        context["banners"] = banners
        context["banners_cache_value"] = MAIN_BANNERS_CACHE
        return context


class MarketMain(TemplateView, BannerMixin):
    """Представление главной страницы магазина"""

    template_name = "main/index.html"
