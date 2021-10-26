import random

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

    categories = GoodCategory.objects.only('name', 'image').filter(active=True, parent_category=None).order_by(
        'order_index')
    return categories
