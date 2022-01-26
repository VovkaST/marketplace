import factory
from main.models import GoodCategory


class GoodCategoryFactory(factory.django.DjangoModelFactory):
    """
    При инициализации объекта создает продавца с порядковым номером по счету создания
    """

    class Meta:
        model = GoodCategory

    name = factory.Sequence(lambda n: f"Category name {n}")
    order_index = factory.Sequence(lambda n: n)
