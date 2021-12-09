from app_sellers.models import Balances, Goods, GoodsImage, Sellers
from django.views import generic
from main.views import CacheSettingsMixin
from services.sellers import get_choices_sellers_by_good


class SellerDetailView(generic.DetailView, CacheSettingsMixin):
    model = Sellers


class GoodDetailView(generic.DetailView):
    model = Goods
    template_name = "app_sellers/product_detail.html"
    context_object_name = "detail_product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["seller"] = get_choices_sellers_by_good(obj.id)
        context["balance"] = Balances.objects.filter(good=obj.id)

        return context
