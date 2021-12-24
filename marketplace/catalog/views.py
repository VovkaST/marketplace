import django_filters
from app_sellers.models import Balances, Goods
from django.db.models.functions import Coalesce
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django_filters.widgets import BooleanWidget, LinkWidget, RangeWidget

# fmt: off
from django.db.models import (
    Count,
    Exists,
    Min,
    OuterRef,
    Sum,
    Value,
)  # isort:skip

from main.views import CategoryMixin, PageInfoMixin


class CatalogFilter(django_filters.FilterSet):
    min_price = django_filters.RangeFilter(widget=RangeWidget(), label=_('Price range'))
    name = django_filters.CharFilter(lookup_expr="icontains", label=_('Name'))
    on_balance = django_filters.BooleanFilter(widget=BooleanWidget(), label=_('On balance'))
    on_sale = django_filters.BooleanFilter(widget=BooleanWidget(), label=_('On sale'))

    o = django_filters.OrderingFilter(
        fields=(_("reviews_count"), _("sales"), _("min_price")),
        widget=LinkWidget,
    )

    class Meta:
        model = Goods
        fields = ["name"]


class FilteredListView(CategoryMixin, PageInfoMixin, ListView):
    page_title = _('Catalog')
    filterset_class = None

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context["filterset"] = self.filterset
        return context


class CatalogView(FilteredListView):

    # модель Balances вместо других моделей используется для отладки, пока нет моделей GoodsInStocks и Reviews

    # здесь должно быть  stocks_subquery = GoodsInStocks.objects.filter(good=OuterRef('pk'))
    stocks_subquery = Balances.objects.filter(good=OuterRef("pk"))

    #               здесь должно быть reviews_count=Count("reviews_count")
    queryset = Goods.objects.annotate(
        reviews_count=Count("good_balance"),
        min_price=Min("good_balance__price"),
        on_sale=Exists(stocks_subquery),
        sum_balance=Coalesce(Sum("good_balance__quantity"), Value(0)),
    ).filter(good_balance__isnull=False)

    template_name = "catalog/catalog.html"
    context_object_name = "goods_list"
    filterset_class = CatalogFilter
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        if "pk" in self.kwargs:
            queryset = queryset.filter(category__id=self.kwargs["pk"])
        return queryset
