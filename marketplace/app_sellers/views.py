from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views import View, generic

from app_sellers.models import Balances, Goods, Reviews, Sellers
from app_sellers.forms import ReviewForm
from main.views import CategoryMixin, PageInfoMixin
from services.sellers import get_choices_sellers_by_good
from services.view_history import add_goods_to_view_history


class SellerDetailView(PageInfoMixin, CategoryMixin, generic.DetailView):
    model = Sellers

    @property
    def page_title(self):
        obj = self.get_object()
        return obj.name


class GoodDetailView(PageInfoMixin, CategoryMixin, generic.DetailView):
    model = Goods
    template_name = "app_sellers/product_detail.html"
    context_object_name = "detail_product"

    @property
    def page_title(self):
        obj = self.get_object()
        return obj.name

    def get_queryset(self):
        return super().get_queryset().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        balances = Balances.objects.filter(good=obj.id)\
            .values("id", "seller__name", "quantity", "price")\
            .order_by('price')
        context.update({
            'good_categories': ({
                obj.category.id: obj.category.name,
                obj.category.parent_id: obj.category.parent.name if obj.category.parent_id else None,
            }),
            'seller': get_choices_sellers_by_good(obj.id),
            'balance': balances[0],
            'other_balances': balances[1:],
            'review_form': ReviewForm(),
            'description': obj.description.all().values('feature__value', 'value')
        })
        if self.request.user.is_authenticated:
            add_goods_to_view_history(self.request.user, obj)
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


class SellersListView(PageInfoMixin, CategoryMixin, generic.ListView):
    """Список продавцов"""

    page_title = _('Our sellers')
    model = Sellers
    context_object_name = 'sellers_list'
