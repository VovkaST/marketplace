from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from app_sellers.models import (
    Balances,
    Goods,
    GoodsDescriptionsValues,
    RatingStar,
    Reviews,
    Sellers,
)
from services.cache import reset_seller_page_cache


class GoodsDescriptionsFilter(admin.SimpleListFilter):
    title = _('Description type')
    parameter_name = 'type'

    def queryset(self, request, queryset):
        if self.value() == 'cat':
            return queryset.filter(feature__isnull=True)
        if self.value() == 'val':
            return queryset.filter(feature__isnull=False)

    def lookups(self, request, model_admin):
        return (
            ('cat', _('Categories')),
            ('val', _('Values')),
        )


@admin.register(Sellers)
class SellersAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        reset_seller_page_cache(seller=obj)


@admin.register(GoodsDescriptionsValues)
class GoodsDescriptionsValuesAdmin(admin.ModelAdmin):
    list_display = ('value', 'feature', )
    list_filter = (GoodsDescriptionsFilter, )

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == 'feature':
            return db_field.remote_field.model.objects.filter(feature__isnull=True)
        return super().get_field_queryset(db, db_field, request)


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    pass


@admin.register(Balances)
class BalancesAdmin(admin.ModelAdmin):
    pass


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    model = Reviews
    list_display = ["user", "good_review", "comment", "star", "crated_at"]


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    model = RatingStar
    list_display = [
        "value",
    ]
