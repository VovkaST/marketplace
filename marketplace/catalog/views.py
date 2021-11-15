import django_filters
from app_sellers.models import Goods
from django.views.generic import ListView
from django_filters.widgets import LinkWidget, RangeWidget


class CatalogFilter(django_filters.FilterSet):

    sales = django_filters.RangeFilter(widget=RangeWidget())

    # manufacturer = django_filters.ModelChoiceFilter(queryset=Manufacturer.objects.all())

    name = django_filters.CharFilter(lookup_expr="icontains")

    # activity = django_filters.BooleanFilter(widget=BooleanWidget())

    o = django_filters.OrderingFilter(fields=["sales", "name"], widget=LinkWidget)

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
    model = Goods
    template_name = "catalog/catalog.html"
    filterset_class = CatalogFilter
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        if "pk" in self.kwargs:
            queryset = queryset.filter(category__id=self.kwargs["pk"])
        return queryset
