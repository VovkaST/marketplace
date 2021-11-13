from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.utils.translation import get_language

from app_sellers.models import Sellers
from services.basket import get_basket_meta
from services.cache_settings import (
    BASKET_TOTAL_SUM_CACHE_PREFIX,
    GOODS_IN_BASKET_CACHE_PREFIX,
    cache_settings,
)


BASKET_LIFE_TIME = cache_settings['basket_life_time']


def reset_seller_page_cache(seller: Sellers):
    """Reset cache on detailed view seller`s page"""
    key = make_template_fragment_key('seller_info', seller.slug)
    cache.delete(key)


def basket_cache_save(session_id, user_id: None, lifetime=BASKET_LIFE_TIME) -> dict:
    """Сохраняет мета-данные пользовательской корзины в кэше.

    :param session_id: Идентификатор сессии.
    :param user_id: Идентификатор пользователя.
    :param lifetime: Время жизни кэша в секундах.
    """
    goods_quantity_cache_key = f'{GOODS_IN_BASKET_CACHE_PREFIX}_{session_id}'
    total_sum_cache_key = f'{BASKET_TOTAL_SUM_CACHE_PREFIX}_{session_id}'
    if goods_quantity_cache_key not in cache \
            or total_sum_cache_key not in cache:
        meta = get_basket_meta(session_id=session_id, user_id=user_id)
        cache.set(goods_quantity_cache_key, meta['goods_quantity'], lifetime)
        cache.set(total_sum_cache_key, meta['total_sum'], lifetime)
        return meta
    return {
        'goods_quantity': cache.get(goods_quantity_cache_key),
        'total_sum': cache.get(total_sum_cache_key),
    }


def basket_cache_clear(session_id: str, username: str = None):
    """Clear user`s basket cache.

    :param session_id: Current session key.
    :param username: Current user`s name.
    """
    user_key = username or session_id
    cache.delete(make_template_fragment_key('basket', (user_key, get_language())))
    cache.delete(f'{GOODS_IN_BASKET_CACHE_PREFIX}_{session_id}')
    cache.delete(f'{BASKET_TOTAL_SUM_CACHE_PREFIX}_{session_id}')
