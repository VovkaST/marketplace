from decimal import Decimal
from typing import Dict, List, Tuple, Union

from django.contrib.auth.models import User
from django.db.models import (
    DecimalField,
    F,
    IntegerField,
    Sum,
)
from django.utils.translation import gettext as _

from app_basket.models import Basket
from app_sellers.models import (
    Balances,
    Goods,
    Sellers,
)
from marketplace.settings import DECIMAL_SUM_TEMPLATE
from services.cache import basket_cache_clear


def is_enough_shop_balances(reservation_id: int, needle_quantity: int) -> bool:
    """Проверка наличия запрашиваемого количества товара на балансе продавца.

    :param reservation_id: Идентификатор баланса.
    :param needle_quantity: Запрашиваемоу количество.
    """
    available = Balances.objects.filter(id=reservation_id).values('quantity').first()
    return available.get('quantity', 0) >= needle_quantity


def patch_item_quantity(user_id: int, session: str, reservation_id: str, quantity: int = 1) -> Tuple[dict, str]:
    """Изменяет количество единиц товара в пользовательской корзине.

    :param user_id: Идентификатор авторизованного пользователя.
    :param session: Строка идентификатора сессии.
    :param reservation_id: Идентификатор баланса продавца.
    :param quantity: Количество единиц товара.
    :return: Данные измененного объекта и сообщение об ошибке.
    """
    obj_data, error = None, None

    try:
        obj = Basket.objects.user_basket(session_id=session, user_id=user_id)\
            .filter(reservation_id=reservation_id)\
            .first()
        if not obj:
            raise Exception(_('Item not found in basket.'))
        obj.quantity = quantity
        obj.save(force_update=True, update_fields=['quantity'])
        obj_data = {
            'good_id': obj.reservation.good_id,
            'available': obj.reservation.quantity,
            'quantity': quantity,
            'price': obj.reservation.price,
            'total_price': (Decimal(quantity) * obj.reservation.price).quantize(DECIMAL_SUM_TEMPLATE),
        }
    except Exception as exc:
        error = exc.args[0]
    return obj_data, error


def patch_item_seller(user_id: int, session: str, reservation_id: str, seller: int = None)\
        -> Tuple[dict, Union[str, None]]:
    """Изменяет продавца товара в пользовательской корзине.

    :param user_id: Идентификатор авторизованного пользователя.
    :param session: Строка идентификатора сессии.
    :param reservation_id: Идентификатор баланса продавца.
    :param seller: ...
    :return: Данные измененного объекта и сообщение об ошибке.
    """
    obj_data, error = None, None

    try:
        obj = Basket.objects.user_basket(session_id=session, user_id=user_id)\
            .filter(reservation_id=reservation_id)\
            .select_related('reservation', 'reservation__seller')\
            .first()
        if not obj:
            raise Exception(_('Item not found in basket.'))
        obj_balance = Balances.objects\
            .filter(seller_id=seller, good=obj.reservation.good)\
            .select_related('seller')\
            .first()
        if not obj_balance:
            raise Exception(_('Seller not found.'))
        obj.reservation = obj_balance
        obj.save(force_update=True, update_fields=['reservation'])
        obj_data = {
            'reservation_id': obj_balance.id,
            'good_id': obj.reservation.good_id,
            'available': obj.reservation.quantity,
            'quantity': obj.quantity,
            'price': obj.reservation.price,
            'total_price': (Decimal(obj.quantity) * obj.reservation.price).quantize(DECIMAL_SUM_TEMPLATE),
            'seller': {
                'id': obj.reservation.seller.id,
                'name': obj.reservation.seller.name,
                'image': None,
            },
        }
    except Exception as exc:
        error = exc.args[0],
    return obj_data, error


def delete_item_from_basket(user_id: int, session: str, reservation_id: str) -> dict:
    """Удаляет товар из пользовательской корзины.

    :param user_id: Идентификатор авторизованного пользователя.
    :param session: Строка идентификатора сессии.
    :param reservation_id: Идентификатор баланса продавца.
    :return: Ошибки в виде словаря.
    """
    error = dict()
    try:
        deleted, _ = Basket.objects.user_basket(session_id=session, user_id=user_id)\
            .filter(reservation_id=reservation_id)\
            .delete()
        if not deleted:
            raise Exception(_('Item not found in basket.'))
    except Exception as exc:
        error.update({
            'message': exc.args[0],
        })
    return error


def add_item_to_basket(user_id: int, session: str, reservation_id: str, quantity: int = 1) -> Tuple[dict, str]:
    """Добавляет товар из баланса продавцов в пользовательскую корзину.

    :param user_id: Идентификатор авторизованного пользователя.
    :param session: Строка идентификатора сессии.
    :param reservation_id: Идентификатор баланса продавца.
    :param quantity: Количество единиц товара.
    :return: Ошибки в виде словаря.
    """
    obj_data, error = None, None
    searchable = {
        'reservation_id': reservation_id,
        'user_id': user_id,
        'session': session,
    }
    try:
        obj, created = Basket.objects.get_or_create(**searchable, defaults={'quantity': quantity})
        if not created:
            return patch_item_quantity(
                user_id=user_id, session=session, reservation_id=reservation_id, quantity=obj.quantity + quantity
            )
        obj_data = {
            'good_id': obj.reservation.good_id,
            'available': obj.reservation.quantity,
            'quantity': quantity,
            'price': obj.reservation.price,
            'total_price': (Decimal(quantity) * obj.reservation.price).quantize(DECIMAL_SUM_TEMPLATE),
        }
    except Exception as exc:
        error = exc.args[0]
    return obj_data, error


def get_basket_meta(session_id: str, user_id: int = None, items: bool = False) -> Dict[str, str]:
    """Получает количественные показатели пользовательской корзины.

    :param session_id: Идентификатор сессии.
    :param user_id: Идентификатор пользователя.
    :param items: Флаг необходимости получения списка товаров.
    :return: Мета-данные пользовательской корзины.
    """
    total_sum = 0
    items_list = list()
    if not items:
        data = Basket.objects\
            .user_basket(user_id=user_id, session_id=session_id)\
            .aggregate(
                goods_quantity=Sum('quantity', output_field=IntegerField()),
                total_sum=Sum(
                    F('quantity') * F('reservation__price'),
                    output_field=DecimalField(decimal_places=2, max_digits=19)
                )
            )
        goods_quantity = data['goods_quantity'] or 0
        total_sum = Decimal(data['total_sum'] or 0).quantize(DECIMAL_SUM_TEMPLATE)
    else:
        data = Basket.objects \
            .user_basket(user_id=user_id, session_id=session_id) \
            .select_related('reservation__good', 'reservation__seller')
        goods_quantity = len(data)
        for item in data:
            total_price = Decimal(item.quantity) * item.reservation.price
            item_data = {
                'reservation_id': item.reservation_id,
                'good_id': item.reservation.good_id,
                'quantity': int(item.quantity or 1),
                'price': item.reservation.price,
                'total_price': total_price,
                'name': item.reservation.good.name,
                'image': item.reservation.good.good_images,
                'available': item.reservation.quantity,
                'is_enough': item.reservation.quantity and item.quantity <= item.reservation.quantity,
                'seller': {
                    'id': item.reservation.seller.id,
                    'name': item.reservation.seller.name,
                    'image': None,
                },
                'other_sellers': get_available_sellers(good=item.reservation.good)
            }
            items_list.append(item_data)
            total_sum += total_price
    return {
        'goods_quantity': goods_quantity,
        'total_sum': total_sum,
        'items': items_list,
    }


def get_available_sellers(good: Goods) -> Dict[int, str]:
    sellers = Sellers.objects\
        .filter(balance_owner__good_id=good.id, balance_owner__quantity__gt=0)\
        .values('id', 'name', 'balance_owner__price')
    return {seller['id']: f'{seller["name"]} ({seller["balance_owner__price"]})' for seller in sellers}


def merge_baskets(old_session: str, new_session: str, user: User):
    """Объединение корзин неавторизованного пользователя с
    корзиной после авторизации. Если у него были до этого
    отложены товары в корзине, то корзины сливаются.

    :param old_session: id сессии до авторизации.
    :param new_session: id сессии после авторизации.
    :param user: экземпляр авторизованного пользователя.
    """
    Basket.objects.user_basket(session_id=old_session, user_id=user.id).update(session=new_session)
    anon_user_goods = Basket.objects.filter(session=old_session)
    duplicates = list()
    for good in anon_user_goods:
        exist_good = Basket.objects.user_basket(user_id=user.id).filter(reservation=good.reservation).first()
        if exist_good:
            exist_good.quantity += good.quantity
            exist_good.save(force_update=True, update_fields=['quantity'])
            duplicates.append(good.id)
        else:
            good.session = new_session
            good.user = user
            good.save(force_update=True, update_fields=['session', 'user'])
    if duplicates:
        Basket.objects.filter(id__in=duplicates).delete()
    if duplicates or anon_user_goods:
        basket_cache_clear(session_id=old_session)
