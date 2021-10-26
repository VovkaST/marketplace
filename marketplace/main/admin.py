from django.contrib import admin

from .models import GoodCategory, Banner


@admin.register(GoodCategory)
class StockTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'deleted', 'active', 'order_index')


class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "created_date", "activity")


admin.site.register(Banner, BannerAdmin)
