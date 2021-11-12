from decimal import Decimal

from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum, F, FloatField
from django.utils import timezone

from app_basket.models import Basket
from marketplace.settings import DECIMAL_SUM_TEMPLATE


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


def add_item_to_basket(user: User, session: str, reservation_id: str, quantity: int = 1) -> dict:
    """Добавляет товар из баланса продавцов в пользовательскую корзину.

    :param user: Экземпляр АВТОРИЗОВАННОГО пользователя или None
                 в случае анонимного пользователя.
    :param session: Строка идентификатора сессии.
    :param reservation_id: Идентификатор баланса продавца.
    :param quantity: Количество единиц товара.
    :return: Errors dict.
    """
    error = dict()
    searchable = {
        'reservation_id': reservation_id,
        'user': user,
        'session': session
    }
    defaults = {
        'quantity': quantity,
        'modified_at': timezone.now(),
    }
    try:
        obj, created = Basket.objects.get_or_create(defaults=defaults, **searchable)
        if not created:
            obj.quantity += quantity
            obj.save(force_update=True)
    except Exception as exc:
        error = {
            'message': exc.args[0],
        }
    return error


def get_basket_total_sum(request: WSGIRequest) -> Decimal:
    """Calculate quantity of goods in user Basket.

    :param request: http-request instance.
    :return: quantity of goods in user Basket.
    """
    quantity = Basket.objects\
        .user_basket(request=request)\
        .aggregate(total=Sum(F('quantity') * F('reservation__price'), output_field=FloatField()))
    return Decimal(quantity['total'] or 0).quantize(DECIMAL_SUM_TEMPLATE)
