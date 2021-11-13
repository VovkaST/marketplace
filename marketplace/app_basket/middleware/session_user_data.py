from services.cache import basket_cache_save


class SessionDataCollector:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.create()
        meta = basket_cache_save(session_id=request.session.session_key, user_id=request.user.id)
        request.goods_in_basket = meta['goods_quantity']
        request.basket_total_sum = meta['total_sum']
        return self.get_response(request)
