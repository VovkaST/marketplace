from django.contrib import admin

from app_sellers.models import (
    Balances,
    Goods,
    GoodsDescriptionsValues,
    GoodsImage,
    RatingStar,
    Reviews,
    Sellers,
)
from services.cache import reset_seller_page_cache


@admin.register(Sellers)
class SellersAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        reset_seller_page_cache(seller=obj)


@admin.register(GoodsDescriptionsValues)
class GoodsDescriptionsValuesAdmin(admin.ModelAdmin):
    list_display = ('value', 'feature', )


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
