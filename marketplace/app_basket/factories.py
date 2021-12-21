import factory
from app_basket.models import Basket
from app_sellers.factories import BalancesFactory
from profiles.factories import UserFactory


class BasketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Basket

    user = factory.SubFactory(UserFactory)
    session = factory.Sequence(lambda n: n)
    reservation = factory.SubFactory(BalancesFactory)
    quantity = factory.Sequence(lambda n: n)
