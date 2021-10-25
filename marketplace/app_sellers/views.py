from django.views import generic

from app_sellers.models import Sellers
from services.cache_settings import SELLER_INFO_CACHE
from services.decorators import context_data


@context_data(context={
    'seller_info_cache_life_time': SELLER_INFO_CACHE,
})
class SellerDetailView(generic.DetailView):
    model = Sellers
