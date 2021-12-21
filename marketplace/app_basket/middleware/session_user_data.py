from services.basket import get_basket_meta
from services.cache import (
    basket_cache_save,
    get_basket_cache,
    get_order_availability_cache,
)
from services.orders import is_incomplete_order


class SessionDataCollector:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.create()
        self.basket_info(request)
        self.order_info(request)
        return self.get_response(request)

    def basket_info(self, request):
        """Собирает данные по корзине (кол-во товаров, общая стоимость).
        Если в кэше отсутствуют, то получает их из БД, сохраняет и
        присваивает атрибутам (goods_in_basket, basket_total_sum)
        запроса (request) соответствующие значения.
        """
        session_id = request.session.session_key
        keys = [
            'goods_quantity',
            'total_sum',
        ]
        meta = get_basket_cache(session_id=session_id, keys=keys)
        if not any(meta.values()):
            meta = get_basket_meta(session_id=session_id, user_id=request.user.id)
            basket_cache_save(session_id=session_id, **meta)
        request.goods_in_basket = meta['goods_quantity']
        request.basket_total_sum = meta['total_sum']

    def order_info(self, request):
        """Собирает данные по заказу (наличие незавершенного заказа).
        Если в кэше отсутствует, то ищет его в БД, сохраняет и
        присваивает атрибуту (is_incomplete_order) запроса (request)
        соответствующее значение.
        """
        incomplete_order_cache = get_order_availability_cache(session_id=request.session.session_key)
        if not incomplete_order_cache:
            incomplete_order_cache = is_incomplete_order(user=request.user)
        request.is_incomplete_order = incomplete_order_cache
