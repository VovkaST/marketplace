from decimal import Decimal

import factory

# fmt: off
from app_sellers.models import Balances, Goods, GoodsDescriptionsValues, Sellers  # isort:skip
from main.factories import GoodCategoryFactory  # isort:skip
# fmt: on


class SellersFactory(factory.django.DjangoModelFactory):
    """
    При инициализации объекта создает продавца с порядковым номером по счету создания
    """

    class Meta:
        model = Sellers
        django_get_or_create = ("slug",)

    slug = factory.Sequence(lambda n: f"Slug_{n}")
    name = factory.Sequence(lambda n: f"Seller name {n}")
    address = factory.Sequence(lambda n: f"Seller address {n}")
    email = factory.Sequence(lambda n: f"seller{n}@test.test")
    phone = factory.Sequence(lambda n: f"Phone {n}")
    description = factory.Sequence(lambda n: f"Seller description {n}")


class GoodsDescriptionsValuesFactory(factory.django.DjangoModelFactory):
    """
    Создает описание товара с объектом родителем описания
    Для того чтобы избежать бесконечную рекурсию следует использовать конструкцию:
    GoodsDescriptionsValuesFactory(feature__feature=None)
    """

    class Meta:
        model = GoodsDescriptionsValues

    value = factory.Sequence(lambda n: f"Description value {n}")
    feature = factory.SubFactory("app_sellers.factories.GoodsDescriptionsValuesFactory")


class GoodsFactory(factory.django.DjangoModelFactory):
    """
    Создает объект товара
    """

    class Meta:
        model = Goods
        django_get_or_create = ("pk",)

    pk = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f"Good name {n}")
    category = factory.SubFactory(GoodCategoryFactory)


class BalancesFactory(factory.django.DjangoModelFactory):
    """
    Создает объект наличия товара с товаром и несколькими продавцами для этого товара
    """

    class Meta:
        model = Balances
        django_get_or_create = ("seller", "good")

    seller = factory.SubFactory(SellersFactory)
    good = factory.SubFactory(GoodsFactory)
    quantity = factory.Sequence(lambda n: 10 * (n + 1))
    price = factory.Sequence(lambda n: Decimal(500) * (n + 1))
