from django.core.handlers.wsgi import WSGIRequest

from app_comparison.models import Comparison
from services.basket import get_basket_meta
from services.cache import (
    basket_cache_save,
    comparison_cache_save,
    get_basket_cache,
    get_comparison_cache,
    get_order_cache,
    order_cache_save,
)
from services.orders import is_not_confirmed_order, is_not_payed_order


class SessionDataCollector:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        if not request.session.session_key:
            request.session.create()
        self.basket_info(request)
        self.order_info(request)
        self.comparison_info(request)
        return self.get_response(request)

    def basket_info(self, request: WSGIRequest):
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

    def order_info(self, request: WSGIRequest):
        """Собирает данные по заказу (наличие незавершенного заказа).
        Если в кэше отсутствует, то ищет его в БД, сохраняет и
        присваивает атрибуту (is_incomplete_order) запроса (request)
        соответствующее значение.
        """
        order_cache = get_order_cache(session_id=request.session.session_key)
        if not order_cache:
            order_cache['is_not_confirmed'] = is_not_confirmed_order(user=request.user)
            order_cache['is_not_payed'] = is_not_payed_order(user=request.user)
            order_cache_save(session_id=request.session.session_key, **order_cache)
        request.is_not_confirmed_order = order_cache['is_not_confirmed']
        request.is_not_payed_order = order_cache['is_not_payed']

    def comparison_info(self, request: WSGIRequest):
        """Получает данные о количестве товаров в пользовательском
        списке сравнения."""
        session_key = request.session.session_key
        count = get_comparison_cache(session_id=session_key)
        if count is None:
            user_data = {
                'user_id': request.user.id if request.user.is_authenticated else None,
                'session': session_key,
            }
            count = Comparison.objects.user_comparison(**user_data).count()
            comparison_cache_save(session=session_key, value=count)
        request.comparison_count = count
