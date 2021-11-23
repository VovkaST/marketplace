import django_filters
from app_sellers.models import Balances, Goods, Sellers
from django.db.models.functions import Coalesce
from django.views.generic import ListView
from django_filters.widgets import BooleanWidget, LinkWidget, RangeWidget

# fmt: off
from django.db.models import (Case, Count, Exists, Min, OuterRef, Sum, Value,  # isort:skip
                              When)  # isort:skip


class CatalogFilter(django_filters.FilterSet):
    min_price = django_filters.RangeFilter(widget=RangeWidget())
    name = django_filters.CharFilter(lookup_expr="icontains")
    on_balance = django_filters.BooleanFilter(widget=BooleanWidget())
    on_sale = django_filters.BooleanFilter(widget=BooleanWidget())

    o = django_filters.OrderingFilter(
        fields=("reviews_count", "sales", "min_price"),
        # field_labels={
        #     'reviews_count': 'Qty of reviews',
        # },
        widget=LinkWidget,
    )

    class Meta:
        model = Goods
        fields = ["name"]


class FilteredListView(ListView):
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
    ).annotate(
        on_balance=Case(When(sum_balance__gt=0, then=Value(True)), default=Value(False))
    )

    template_name = "catalog/catalog.html"
    context_object_name = "goods_list"
    filterset_class = CatalogFilter
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        if "pk" in self.kwargs:
            queryset = queryset.filter(category__id=self.kwargs["pk"])
        return queryset
