import django_filters
from app_sellers.models import Balances, Goods
from django.db.models import Count
from django.views.generic import ListView
from django_filters.widgets import LinkWidget, RangeWidget


class CatalogFilter(django_filters.FilterSet):
    sales = django_filters.RangeFilter(widget=RangeWidget())
    name = django_filters.CharFilter(lookup_expr="icontains")

    reviews_count = django_filters.RangeFilter(widget=RangeWidget())

    # manufacturer = django_filters.ModelChoiceFilter(queryset=Manufacturer.objects.all())
    # activity = django_filters.BooleanFilter(widget=BooleanWidget())

    o = django_filters.OrderingFilter(
        fields=(
            # ('reviews_count', 'reviews_count'),
            "reviews_count",
            "sales",
            "name",
        ),
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
    # model = Goods
    # queryset = Goods.objects.annotate_with_reviews_count()
    queryset = Goods.objects.annotate(reviews_count=Count("good_balance"))
    template_name = "catalog/catalog.html"
    filterset_class = CatalogFilter
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        if "pk" in self.kwargs:
            queryset = queryset.filter(category__id=self.kwargs["pk"])
        return queryset
