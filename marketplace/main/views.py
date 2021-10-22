from django.views.generic.base import ContextMixin, TemplateView

from marketplace.services.main_page import get_banners


class BannerMixin(ContextMixin):
    """Выбор баннеров и занесение их в context"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banners = get_banners()
        context["banners"] = banners
        return context


class MarketMain(TemplateView, BannerMixin):
    """Представление главной страницы магазина"""

    template_name = "main/index.html"
