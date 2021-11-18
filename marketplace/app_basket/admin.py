from django.contrib import admin

from app_basket.models import Basket


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass
