from decimal import Decimal

import factory

# fmt: off
from app_sellers.models import Balances, Goods, GoodsDescriptionsValues, Sellers  # isort:skip
from main.factories import GoodCategoryFactory  # isort:skip
# fmt: on


class SellersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sellers

    name = factory.Sequence(lambda n: f"Seller name {n}")
    address = factory.Sequence(lambda n: f"Seller address {n}")
    email = factory.Sequence(lambda n: f"seller{n}@test.test")
    phone = factory.Sequence(lambda n: f"Phone {n}")
    description = factory.Sequence(lambda n: f"Seller description {n}")


class GoodsDescriptionsValuesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoodsDescriptionsValues

    value = factory.Sequence(lambda n: f"Description value {n}")


class GoodsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goods

    name = factory.Sequence(lambda n: f"Good name {n}")
    category = factory.SubFactory(GoodCategoryFactory)
    description = factory.SubFactory(GoodsDescriptionsValuesFactory)


class BalancesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Balances

    seller = factory.SubFactory(SellersFactory)
    good = factory.SubFactory(GoodsFactory)
    quantity = factory.Sequence(lambda n: 10 * n)
    price = factory.Sequence(lambda n: Decimal(500) * n)
