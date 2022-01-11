from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.utils.translation import get_language

from app_sellers.models import Sellers
from services.cache_settings import cache_settings


BASKET_LIFE_TIME = cache_settings['basket_life_time']


def reset_seller_page_cache(seller: Sellers):
    """Reset cache on detailed view seller`s page"""
    key = make_template_fragment_key('seller_info', seller.slug)
    cache.delete(key)


def basket_cache_save(session_id: str, lifetime=BASKET_LIFE_TIME, **kwargs):
    """Сохраняет мета-данные пользовательской корзины в кэше.

    :param session_id: Идентификатор сессии.
    :param lifetime: Время жизни кэша в секундах.
    """
    for key, value in kwargs.items():
        if value is not None:
            cache.set(f'basket_{session_id}_{key}', value, lifetime)


def get_basket_cache(session_id: str, keys=None) -> dict:
    """Получает значения из кэша для переменных, указанных
    в списке keys.

    :param session_id: Идентификатор сессии.
    :param keys: Список имен сохраненных переменных.
    :return: Словарь восстановленных переменных.
    """
    return {
        key: cache.get(f'basket_{session_id}_{key}')
        for key in keys
    }


def basket_cache_clear(session_id: str = None, username: str = None, keys=None):
    """Clear user`s basket cache.

    :param session_id: Current session key.
    :param username: Current user`s name.
    :param keys: Список имен сохраненных переменных.
    """
    if not keys:
        keys = ['goods_quantity', 'total_sum', 'items']
    user_key = username or session_id
    cache.delete(make_template_fragment_key('basket', (user_key, get_language())))
    for key in keys:
        cache.delete(f'basket_{session_id}_{key}')


def get_order_availability_cache(session_id: str) -> bool:
    """Получить кэш флага незавершенного заказа."""
    return cache.get(f'order_availability_{session_id}')


def order_availability_cache_save(session_id: str, value: bool):
    """Сохранить флаг незавершенного заказа в кэше."""
    return cache.set(f'order_availability_{session_id}', value)


def order_availability_cache_clear(session_id: str):
    """Удалить флаг незавершенного заказа в кэше."""
    return cache.delete(f'order_availability_{session_id}')


def get_comparison_cache(session_id: str) -> int:
    """Получить кэш количества товаров в списке сравнения."""
    return cache.get(f'comparison_{session_id}')


def comparison_cache_save(session: str, value: int):
    """Сохранить количество товаров в списке сравнения в кэш."""
    return cache.set(f'comparison_{session}', value)


def comparison_cache_clear(session: str):
    """Удалить список сравнения товаров из кэша."""
    # todo: кэш страницы
    return cache.delete(f'comparison_{session}')
