from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from app_sellers.models import Sellers


def reset_seller_page_cache(seller: Sellers):
    """Reset cache on detailed view seller`s page"""
    key = make_template_fragment_key('seller_info', seller.slug)
    cache.delete(key)
