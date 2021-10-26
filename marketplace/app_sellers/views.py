from django.views import generic

from app_sellers.models import Sellers
from main.views import CacheSettingsMixin


class SellerDetailView(generic.DetailView, CacheSettingsMixin):
    model = Sellers
