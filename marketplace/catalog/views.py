import django_filters

from app_sellers.models import Goods
from django.utils.translation import gettext as _
from django.views.generic import ListView
from django_filters.widgets import BooleanWidget, LinkWidget, RangeWidget

from main.views import CategoryMixin, PageInfoMixin
from services.goods import GoodsMinPriceMixin


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


class CatalogView(GoodsMinPriceMixin, FilteredListView):
    queryset = Goods.objects\
        .filter(good_balance__isnull=False)\
        .values('id', 'name', 'category__name')

    template_name = "catalog/catalog.html"
    context_object_name = "goods_list"
    filterset_class = CatalogFilter
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        if "pk" in self.kwargs:
            queryset = queryset.filter(category__id=self.kwargs["pk"])
        return queryset
