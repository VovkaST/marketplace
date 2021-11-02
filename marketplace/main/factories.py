import factory
from django.core.files.base import ContentFile
from main.models import GoodCategory


class GoodCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoodCategory

    name = factory.Sequence(lambda n: f"Category name {n}")
    image = factory.Sequence(
        lambda n: ContentFile(
            factory.django.ImageField()._make_data({"width": 1024, "height": 768}),
            f"image{n}.jpg",
        )
    )
    deleted = False
    active = True
    order_index = factory.Sequence(lambda n: n)
