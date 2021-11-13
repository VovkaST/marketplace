from decimal import Decimal

from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import DecimalField, F, IntegerField, Sum
from django.utils import timezone
from django.utils.translation import gettext as _

from app_basket.models import Basket
from marketplace.settings import DECIMAL_SUM_TEMPLATE


def is_enough_shop_balances(basket) -> bool:
    """Check balances for sufficiency of goods.

    :param basket: Iterable user`s basket items.
    :return: Is balances is enough or not.
    """
    return all([goods_item.quantity >= goods_item.balance.quantity for goods_item in basket])


def perform_purchase(request: WSGIRequest):
    pass


def patch_item_in_basket(user: User, session: str, reservation_id: str, quantity: int = 1) -> dict:
    """Patch goods item quantity in user`s basket.

    :param request: http-request instance.
    :param balance_id_key: Balance ID key name in request POST-data.
    :return: Errors dict.
    """
    error = dict()
    searchable = {
        'reservation_id': reservation_id,
        'user': user,
        'session': session
    }
    try:
        updated = Basket.objects.filter(**searchable).update(quantity=quantity)
        if not updated:
            raise Exception(_('Item not found in basket.'))
    except Exception as exc:
        error = {
            'message': exc.args[0],
        }
    return error


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


def get_basket_meta(session_id: str, user_id=None) -> dict:
    """Получает количественные показатели пользовательской корзины.

    :param session_id: Идентификатор сессии.
    :param user_id: Идентификатор пользователя.
    :return: quantity of goods in user Basket.
    """
    meta = Basket.objects\
        .user_basket(user_id=user_id, session_id=session_id)\
        .aggregate(
            goods_quantity=Sum('quantity', output_field=IntegerField()),
            total_sum=Sum(
                F('quantity') * F('reservation__price'),
                output_field=DecimalField(decimal_places=2, max_digits=19)
            )
        )
    return {
        'goods_quantity': meta['goods_quantity'] or 0,
        'total_sum': Decimal(meta['total_sum'] or 0).quantize(DECIMAL_SUM_TEMPLATE),
    }
