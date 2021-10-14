from django.contrib import admin

from app_stocks.models import (
    StockMethod,
    Stocks,
    StockType,
)


@admin.register(StockType)
class StockTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(StockMethod)
class StockMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(Stocks)
class StocksAdmin(admin.ModelAdmin):
    pass
