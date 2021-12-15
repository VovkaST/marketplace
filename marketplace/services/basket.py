from decimal import Decimal
from typing import List, Tuple

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import (
    DecimalField,
    F,
    IntegerField,
    Sum,
)
from django.utils.translation import gettext as _

from app_basket.forms import BasketFormSet
from app_basket.models import Basket
from app_sellers.models import (
    Balances,
    Goods,
    Sellers,
)
from app_orders.models import (
    OrderItems,
    Orders,
)
from marketplace.settings import DECIMAL_SUM_TEMPLATE
from services.cache import basket_cache_clear


def is_enough_shop_balances(basket) -> bool:
    """Check balances for sufficiency of goods.

    :param basket: Iterable user`s basket items.
    :return: Is balances is enough or not.
    """
    return all([goods_item.quantity >= goods_item.balance.quantity for goods_item in basket])


def patch_item_quantity(session: str, reservation_id: str, quantity: int = 1) -> tuple:
    """Изменяет количество единиц товара в пользовательской корзине.

    :param session: Строка идентификатора сессии.
    :param reservation_id: Идентификатор баланса продавца.
    :param quantity: Количество единиц товара.
    :return: Данные измененного объекта и сообщение об ошибке.
    """
    obj_data, error = None, None

    searchable = {
        'reservation_id': reservation_id,
        'session': session,
    }
    try:
        obj = Basket.objects.filter(**searchable).select_related('reservation').first()
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


def patch_item_seller(session: str, reservation_id: str, seller: int = None) -> tuple:
    """Изменяет продавца товара в пользовательской корзине.

    :param session: Строка идентификатора сессии.
    :param reservation_id: Идентификатор баланса продавца.
    :param seller: ...
    :return: Данные измененного объекта и сообщение об ошибке.
    """
    obj_data, error = None, None

    searchable = {
        'reservation_id': reservation_id,
        'session': session,
    }
    try:
        obj = Basket.objects.filter(**searchable).select_related('reservation', 'reservation__seller').first()
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


def delete_item_from_basket(session: str, reservation_id: str) -> dict:
    """Удаляет товар из пользовательской корзины.

    :param session: Строка идентификатора сессии.
    :param reservation_id: Идентификатор баланса продавца.
    :return: Ошибки в виде словаря.
    """
    error = dict()
    searchable = {
        'reservation_id': reservation_id,
        'session': session
    }
    try:
        deleted, _ = Basket.objects.filter(**searchable).delete()
        if not deleted:
            raise Exception(_('Item not found in basket.'))
    except Exception as exc:
        error.update({
            'message': exc.args[0],
        })
    return error


def add_item_to_basket(user: User, session: str, reservation_id: str, quantity: int = 1) -> tuple:
    """Добавляет товар из баланса продавцов в пользовательскую корзину.

    :param user: Экземпляр пользователя.
    :param session: Строка идентификатора сессии.
    :param reservation_id: Идентификатор баланса продавца.
    :param quantity: Количество единиц товара.
    :return: Ошибки в виде словаря.
    """
    obj_data, error = None, None
    searchable = {
        'reservation_id': reservation_id,
        'user_id': user.id if user else None,
        'session': session,
    }
    try:
        obj, created = Basket.objects.get_or_create(**searchable, defaults={'quantity': quantity})
        if not created:
            return patch_item_quantity(
                session=session, reservation_id=reservation_id, quantity=obj.quantity + quantity
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


def get_basket_meta(session_id: str, user_id=None, items=False) -> dict:
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
            .user_basket(session_id=session_id) \
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


def get_available_sellers(good: Goods):
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
    Basket.objects.user_basket(user_id=user.id).update(session=new_session)
    anon_user_goods = Basket.objects.filter(session=old_session)
    duplicates = list()
    for good in anon_user_goods:
        exist_good = Basket.objects.user_basket(user_id=user.id).get(reservation=good.reservation)
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
        basket_cache_clear(session_id=old_session, keys=['goods_quantity', 'total_sum', 'items'])


def init_basket_formset(items):
    initial = [
        {
            'reservation_id': item.get('reservation_id'),
            'quantity': item.get('quantity'),
            'good_id': item.get('good_id'),
            'max_quantity': item.get('available', 1),
            'seller': item['seller']['id'],
        }
        for item in items
    ]
    formset = BasketFormSet(
        initial=initial,
        prefix='basket_item'
    )
    [items[i].update({'form': form}) for i, form in enumerate(formset)]
    return formset


def get_order_summary(user: User) -> dict:
    """Собирает словарь сводных данных по Заказу.

    :param user: экземпляр авторизованного пользователя.
    """
    order = Orders.objects.incomplete_order(user=user, related=True)
    return {
        _('Date, time'): order.date_time.strftime('%d %B %Y, %H:%M'),
        _('Receiver'): f'{order.user.last_name} {order.user.first_name} {order.user.profile.patronymic}',
        _('Phone'): order.user.profile.phone_number_formatted,
        _('Total sum'): None,
        _('City'): order.city,
        _('Address'): order.address,
        _('Delivery method'): order.delivery.name,
        _('Payment method'): order.payment.name,
        _('Bank account'): order.bank_account,
    }


def complete_order(user: User, order: Orders) -> Tuple[Orders, List[OrderItems]]:
    """Сохраняет позиции Заказа, подсчитывает общую сумму
    заказа, помещает ее в экземпляр order. Возвращает измененный
    order и созданные экземпляры OrderItems, помечает Заказ
    как "Подтвержденный" (confirmed = True).

    :param user: экземпляр авторизованного пользователя.
    :param order: экземпляр Заказа.
    """
    items = list()
    with transaction.atomic():
        total_sum = 0
        for basket_item in Basket.objects.user_basket(user_id=user.id):
            total_price = Decimal(basket_item.quantity) * basket_item.reservation.price
            data = {
                'order': order,
                'seller': basket_item.reservation.seller,
                'good': basket_item.reservation.good,
                'quantity': basket_item.quantity,
                'price': basket_item.reservation.price,
                'total_price': total_price,
            }
            total_sum += total_price
            items.append(OrderItems.objects.create(**data))
        order.total_sum = total_sum + order.delivery.price
        order.confirmed = True
        Basket.objects.delete_user_basket(user_id=user.id)
    return order, items
