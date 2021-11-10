from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum

from app_basket.models import Basket


def get_goods_quantity_in_basket(request: WSGIRequest) -> int:
    """Calculate quantity of goods in user Basket.

    :param request: http-request instance.
    :return: quantity of goods in user Basket.
    """
    quantity = Basket.objects.user_basket(request=request).aggregate(Sum('quantity'))
    return int(quantity['quantity__sum'] or 0)


def is_enough_shop_balances(basket) -> bool:
    """Check balances for sufficiency of goods.

    :param basket: Iterable user`s basket items.
    :return: Is balances is enough or not.
    """
    return all([goods_item.quantity >= goods_item.balance.quantity for goods_item in basket])


def perform_purchase(request: WSGIRequest):
    pass


def patch_item_in_basket(request: WSGIRequest):
    pass


def delete_item_from_basket(request: WSGIRequest):
    pass


def add_item_to_basket(request):
    pass
