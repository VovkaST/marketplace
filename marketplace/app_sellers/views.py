from django.views import generic

from app_sellers.models import Sellers
from services.cache_settings import SELLER_INFO_CACHE


class SellerDetailView(generic.DetailView):
    model = Sellers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'seller_info_cache_life_time': SELLER_INFO_CACHE,
        })
        return context
