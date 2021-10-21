from django.views import generic

from app_sellers.models import Sellers


class SellerDetailView(generic.DetailView):
    model = Sellers
