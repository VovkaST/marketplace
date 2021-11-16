import random

from app_sellers.models import Goods
from main.models import Banner, GoodCategory


def get_banners():
    """
    Выбор баннеров для отображения на главной странице
    """
    all_active_banners = Banner.objects.filter(activity=True)
    if all_active_banners.count() > 3:
        banners = random.choices(all_active_banners, k=3)
    else:
        banners = all_active_banners
    return banners


def get_categories():
    """
    Получение категорий
    """

    categories = GoodCategory.objects.only('name', 'image').filter(active=True, parent=None).order_by(
        'order_index')
    return categories.all()


def get_top_goods():
    """Получение топ-товаров"""
    return Goods.objects.raw('''
        SELECT b.id "balance_id", b.good_id "id", min(b.price) "price", g.name
          FROM mp_balances b
          JOIN mp_goods g
                ON b.good_id = g.id
         GROUP BY b.good_id
    ''').prefetch_related('category', 'good_images')
