import random

from app_sellers.models import Goods, Sellers
from main.factories import GoodCategoryFactory
from main.models import GoodCategory


def get_random_category(*args):
    """Возвращает id случайной категории."""
    try:
        ids = GoodCategory.objects.all().values("id")
        return random.choice([item["id"] for item in ids])
    except Exception:
        good_category = GoodCategoryFactory()
        return good_category.pk


def get_random_seller(*args):
    """Возвращает id случайного продавца."""
    ids = Sellers.objects.all().values("id")
    return random.choice([item["id"] for item in ids])


def get_random_good(*args):
    """Возвращает id случайного товара."""
    ids = Goods.objects.all().values("id")
    return random.choice([item["id"] for item in ids])
