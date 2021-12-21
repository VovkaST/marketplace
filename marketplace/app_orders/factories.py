import random
from decimal import Decimal

import factory

from app_orders.utils import get_delivery_method, get_payment_method
from app_sellers.factories import GoodsFactory, SellersFactory
from profiles.factories import UserFactory

# fmt: off
from app_orders.models import (   # isort:skip
    DeliveryMethods,   # isort:skip
    OrderItems,   # isort:skip
    Orders,   # isort:skip
    PaymentMethods,  # isort:skip
)  # isort:skip
# fmt: on


MAX_PAYMENTS_METHODS = 2
MAX_DELIVERY_METHODS = 2


class DeliveryMethodsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeliveryMethods

    name = factory.Sequence(lambda n: f"Delivery method name {n}")
    price = factory.Sequence(lambda n: Decimal(10) * (n + 1))


class PaymentMethodsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentMethods

    name = factory.Sequence(lambda n: f"Payment method name {n}")


class OrdersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Orders

    user = factory.SubFactory(UserFactory)
    total_sum = factory.Sequence(lambda n: Decimal(1000) * (n + 1))
    delivery = factory.Sequence(lambda n: get_delivery_method(random.randint(1, MAX_DELIVERY_METHODS)))
    payment = factory.Sequence(lambda n: get_payment_method(random.randint(1, MAX_PAYMENTS_METHODS)))
    payment_state = False
    bank_account = "12345678901234567890"
    city = factory.Sequence(lambda n: f"City {n}")
    address = factory.Sequence(lambda n: f"Address {n}")
    comment = factory.Sequence(lambda n: f"Comment {n}")


class OrderItemsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItems

    order = factory.SubFactory(OrdersFactory)
    seller = factory.SubFactory(SellersFactory)
    good = factory.SubFactory(GoodsFactory)
    quantity = factory.Sequence(lambda n: n)
    price = factory.Sequence(lambda n: Decimal(10) * (n + 1))
    total_price = factory.Sequence(lambda n: Decimal(10) * (n + 1) * n)
