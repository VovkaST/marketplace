from functools import lru_cache

from app_orders.models import DeliveryMethods, PaymentMethods


@lru_cache(maxsize=None)
def get_delivery_method(record_id):
    return DeliveryMethods.objects.get(id=record_id)


@lru_cache(maxsize=None)
def get_payment_method(record_id):
    return PaymentMethods.objects.get(id=record_id)
