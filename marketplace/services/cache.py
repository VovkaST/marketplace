from typing import Callable

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.handlers.wsgi import WSGIRequest

from app_sellers.models import Sellers
from services.basket import get_goods_quantity_in_basket, get_basket_total_sum
from services.cache_settings import (
    BASKET_TOTAL_SUM_CACHE_PREFIX,
    GOODS_IN_BASKET_CACHE_PREFIX,
    cache_settings,
)


BASKET_LIFE_TIME = cache_settings['basket_life_time']


def set_or_get_cache(request: WSGIRequest, lifetime: int, key: str, func: Callable) -> str:
    """Check "key" in cache, set if not exists with
    given "lifetime". Set attribute "attr_name"
    in request instance. Calculate the value by executing
    "func", that receive one parameter - request.

    :param request: http-request instance.
    :param lifetime: life time of cached data in seconds.
    :param key: cache key name.
    :param func: function to calculate cache value.
    :return: Calculated or cached value.
    """
    if not key:
        raise TypeError('One or several keys must be given.')
    if key not in cache:
        value = func(request)
        cache.set(key, value, lifetime)
        return value
    else:
        return cache.get(key)


def reset_seller_page_cache(seller: Sellers):
    """Reset cache on detailed view seller`s page"""
    key = make_template_fragment_key('seller_info', seller.slug)
    cache.delete(key)


def basket_cache(request: WSGIRequest, lifetime=BASKET_LIFE_TIME):
    """Save information about user`s basket in cache.

    :param request: http-request instance.
    :param lifetime: life time of cached data in seconds.
    """
    if not request.session.session_key:
        request.session.create()
    goods_in_basket_cache_key = f'{GOODS_IN_BASKET_CACHE_PREFIX}_{request.session.session_key}'
    basket_total_sum_cache_key = f'{BASKET_TOTAL_SUM_CACHE_PREFIX}_{request.session.session_key}'
    request.goods_in_basket = set_or_get_cache(
        request=request, lifetime=lifetime, key=goods_in_basket_cache_key, func=get_goods_quantity_in_basket
    )
    request.basket_total_sum = set_or_get_cache(
        request=request, lifetime=lifetime, key=basket_total_sum_cache_key, func=get_basket_total_sum
    )


