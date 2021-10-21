import random

from django.views.generic.base import ContextMixin, TemplateView

from .models import Banner


class BannerMixin(ContextMixin):
    """Выбор баннеров и занесение их в context"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_active_banners = Banner.objects.filter(activity=True)
        if all_active_banners.count() > 3:
            banners = random.sample(all_active_banners, 3)
        else:
            banners = all_active_banners
        context["banners"] = banners
        return context


class MarketMain(TemplateView, BannerMixin):
    """Представление главной страницы магазина"""

    template_name = "main/index.html"
