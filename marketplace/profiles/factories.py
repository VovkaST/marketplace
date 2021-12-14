import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"Username{n}")
    first_name = factory.Sequence(lambda n: f"First name {n}")
    last_name = factory.Sequence(lambda n: f"Last name {n}")
    email = factory.Sequence(lambda n: f"user{n}@test.test")
    is_staff = False
    is_active = True
