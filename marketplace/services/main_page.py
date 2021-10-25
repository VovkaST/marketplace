import random

from main.models import Banner


def get_banners():
    """
    Выбор баннеров для отображения на главной странице
    """
    all_active_banners = Banner.objects.filter(activity=True)
    if all_active_banners.count() > 3:
        banners = random.sample(all_active_banners, 3)
    else:
        banners = all_active_banners
    return banners
