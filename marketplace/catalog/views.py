# fmt: off
import django_filters
from app_sellers.models import Goods
from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django_filters.widgets import BooleanWidget, LinkWidget
from main.models import GoodCategory
from main.views import CategoryMixin, PageInfoMixin
from services.goods import (GoodsPriceMixin, get_balances_in_range,
                            get_cheapest_good_price,
                            get_most_expensive_good_price)

# fmt: on

min_price = get_cheapest_good_price()
max_price = get_most_expensive_good_price()


class CatalogFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label=_("Name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-input form-input_full",
                "placeholder": _("Good name"),
            }
        ),
    )
    price = django_filters.CharFilter(
        label=_("Price range"),
        widget=forms.TextInput(
            attrs={
                "class": "range-line",
                "data-type": "double",
                "data-min": min_price,
                "data-max": max_price,
                "data-from": min_price,
                "data-to": max_price,
            }
        ),
        method="filter_price_between",
    )
    on_balance = django_filters.BooleanFilter(
        widget=BooleanWidget(), label=_("On balance"), method="filter_on_balance"
    )

    reviews_filter = django_filters.OrderingFilter(
        fields=((_("reviews_count"), _("Top")),), widget=LinkWidget
    )

    def filter_on_balance(self, queryset, name, value):
        return queryset.filter(good_balance__quantity__gt=0)

    def filter_price_between(self, queryset, name, value):
        return queryset.filter(good_balance__price__range=value.split(";"))

    # o = django_filters.OrderingFilter(
    #     fields=(_("reviews_count"), _("sales"), _("min_price")),
    #     widget=LinkWidget,
    # )

    class Meta:
        model = Goods
        fields = ["name", "price"]


class FilteredListView(CategoryMixin, PageInfoMixin, ListView):
    page_title = _("Catalog")
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


class CatalogView(GoodsPriceMixin, FilteredListView):
    queryset = Goods.objects.existing().values("id", "name", "category__name")
    template_name = "catalog/catalog.html"
    filterset_class = CatalogFilter
    paginate_by = 6

    def get_balances(self, goods_ids, *args, **kwargs):
        if all((kwargs.get("price_min"), kwargs.get("price_max"))):
            return get_balances_in_range(goods_ids=goods_ids, **kwargs)
        return super().get_balances(goods_ids=goods_ids, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if "pk" in self.kwargs:
            return queryset.filter(category__id=self.kwargs["pk"])
        return queryset

    def get_context_data(self, **kwargs):
        goods_ids = self.object_list.all().values_list("id", flat=True)
        from_price, to_price = None, None
        if "price" in self.filterset.data:
            _from_price, _to_price = self.filterset.form.data["price"].split(";")
            attrs = self.filterset.form.fields["price"].widget.attrs
            if attrs["data-min"] != _from_price or attrs["data-max"] != _to_price:
                from_price, to_price = _from_price, _to_price
                attrs.update(
                    {
                        "data-from": _from_price,
                        "data-to": _to_price,
                    }
                )
        context = super().get_context_data(
            goods_ids=goods_ids, price_min=from_price, price_max=to_price, **kwargs
        )
        return context


class CategoryDetailView(CategoryMixin, PageInfoMixin, GoodsPriceMixin, ListView):
    template_name = "catalog/category_detail.html"
    context_object_name = "goods_list"
    category = None

    def get_category(self):
        if not self.category:
            self.category = get_object_or_404(GoodCategory, pk=self.kwargs["pk"])
        return self.category

    @property
    def page_title(self):
        category = self.get_category()
        if category:
            return category.name

    def get_context_data(self, **kwargs):
        category_id = self.kwargs["pk"]
        goods_ids = Goods.objects.in_category(category_id=category_id).values_list(
            "id", flat=True
        )
        context = super().get_context_data(goods_ids=goods_ids, **kwargs)
        context.update({"category": self.get_category()})
        return context

    def get_queryset(self):
        category_id = self.kwargs["pk"]
        return Goods.objects.in_category(category_id=category_id).values(
            "id", "name", "category__name"
        )
