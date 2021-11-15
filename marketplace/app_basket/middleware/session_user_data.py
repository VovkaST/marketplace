from services.basket import get_basket_meta
from services.cache import (
    basket_cache_save,
    get_basket_cache,
)


class SessionDataCollector:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.create()
        keys = [
            'goods_quantity',
            'total_sum',
        ]
        meta = get_basket_cache(session_id=request.session.session_key, keys=keys)
        if not any(meta.values()):
            meta = get_basket_meta(session_id=request.session.session_key, user_id=request.user.id)
            basket_cache_save(session_id=request.session.session_key, user_id=request.user.id, **meta)
        request.goods_in_basket = meta['goods_quantity']
        request.basket_total_sum = meta['total_sum']
        return self.get_response(request)
