# fmt: off
from app_orders.models import (DeliveryMethods, OrderItems, Orders,
                               PaymentMethods)
from django.contrib import admin
from django.contrib.admin import TabularInline

# fmt: on


class OrderItemsInline(TabularInline):
    model = OrderItems


@admin.register(DeliveryMethods)
class DeliveryMethodsAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentMethods)
class PaymentMethodsAdmin(admin.ModelAdmin):
    pass


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("user", "total_sum", "date_time", "payment_state")
    inlines = (OrderItemsInline,)


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ("order", "seller", "good", "quantity", "total_price")
