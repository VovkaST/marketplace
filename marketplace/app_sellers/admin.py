from django.contrib import admin

from app_sellers.models import (
    Balances,
    Goods,
    GoodsDescriptionsValues,
    Sellers,
)


@admin.register(Sellers)
class SellersAdmin(admin.ModelAdmin):
    pass


@admin.register(GoodsDescriptionsValues)
class GoodsDescriptionsValuesAdmin(admin.ModelAdmin):
    pass


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    pass


@admin.register(Balances)
class BalancesAdmin(admin.ModelAdmin):
    pass


