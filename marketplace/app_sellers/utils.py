import random

from app_sellers.models import Sellers, Goods
from main.models import GoodCategory


def get_random_category(*args):
    """Возвращает id случайной категории."""
    ids = GoodCategory.objects.all().values('id')
    return random.choice([item['id'] for item in ids])


def get_random_seller(*args):
    """Возвращает id случайного продавца."""
    ids = Sellers.objects.all().values('id')
    return random.choice([item['id'] for item in ids])


def get_random_good(*args):
    """Возвращает id случайного товара."""
    ids = Goods.objects.all().values('id')
    return random.choice([item['id'] for item in ids])
