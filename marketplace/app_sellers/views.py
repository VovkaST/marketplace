from app_sellers.models import Balances, Goods, GoodsImage, Sellers
from django.views import generic
from main.views import CacheSettingsMixin


class SellerDetailView(generic.DetailView, CacheSettingsMixin):
    model = Sellers


class GoodDetailView(generic.DetailView):
    model = Goods
    template_name = "app_sellers/product_detail.html"
    context_object_name = "detail_product"

    def get_context_data(self, **kwargs):
        context = super(GoodDetailView, self).get_context_data(**kwargs)
        context["images"] = GoodsImage.objects.all()  # TODO
        context["balance"] = Balances.objects.all()  # TODO вопросы в коммене
        return context
