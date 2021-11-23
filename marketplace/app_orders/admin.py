from django.contrib import admin

from app_orders.models import (
    DeliveryMethods,
    OrderItems,
    Orders,
    PaymentMethods,
)


@admin.register(DeliveryMethods)
class DeliveryMethodsAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentMethods)
class PaymentMethodsAdmin(admin.ModelAdmin):
    pass


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    pass
