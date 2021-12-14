from app_sellers.models import Balances, Goods, GoodsImage, Reviews, Sellers
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View, generic
from main.views import CacheSettingsMixin
from services.sellers import get_choices_sellers_by_good

from .forms import ReviewForm


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
        context["review_form"] = ReviewForm()
        return context


class AddReviews(View):
    """Отзывы"""

    def post(self, request, pk, *args, **kwargs):
        form = ReviewForm(request.POST)
        good = Goods.objects.get(id=pk)
        if form.is_valid():
            comment = form.cleaned_data.get("comment")
            Reviews.objects.update_or_create(
                user_id=self.request.user.id,
                good_review=good,
                comment=comment,
                defaults={"star_id": int(request.POST.get("star"))},
            )
            return HttpResponseRedirect("/")
        return HttpResponseRedirect("/")
