from app_sellers.models import Balances
from loguru import logger
from decimal import Decimal
from typing import Tuple, List

from django.contrib.auth.models import User
from django.db import transaction

from app_basket.models import Basket
from app_orders.models import Orders, OrderItems


def get_user_orders(user: User, limit: int):
    """Function to used to get orders from user orders history
    :user: UserObject
    :limit: int
    :return: Queryset[OrderObject(1), OrderObject(2), ...]
    """
    orders_queryset = Orders.objects.filter(user=user)
    if limit:
        if orders_queryset.count() > limit:
            orders_queryset = orders_queryset[:limit]
    return orders_queryset


def is_not_confirmed_order(user: User) -> bool:
    """Возвращает наличие у пользователя user незавершенного заказа."""
    return bool(Orders.objects.not_confirmed_order(user=user))


def is_not_payed_order(user: User) -> bool:
    """Возвращает наличие у пользователя user неоплаченного заказа."""
    return bool(Orders.objects.not_payed_orders(user=user))


def write_off_balances(order_pk: int):
    """Функция производит списание у продавца остатки товара из заказа"""
    order_items = OrderItems.objects.filter(order__pk=order_pk)
    logger.info(order_items)
    for order_item in order_items:
        balance = Balances.objects.get(seller=order_item.seller, good=order_item.good)
        balance.quantity -= order_item.quantity
        balance.save()


def is_enough_goods_on_balance(order_pk: int):
    """Функция проверяет достаточно ли у продавца товара для списания"""
    order_items = OrderItems.objects.filter(order__pk=order_pk)
    response = {"status": True, "message": ""}
    for order_item in order_items:
        try:
            balance = Balances.objects.get(
                seller=order_item.seller, good=order_item.good
            )
            if balance.quantity >= order_item.quantity and response["status"]:
                response[
                    "message"
                ] += f"{balance.good} is enough in {balance.seller} | \n"
            else:
                response["status"] = False
                response[
                    "message"
                ] += f"{balance.good} is not enough in {balance.seller} | \n"
        except Balances.DoesNotExist:
            response["status"] = False
            response[
                "message"
            ] += f"{order_item.good} doesn`t exists in {order_item.seller} | \n"
    return response


def get_order_summary(order: Orders) -> dict:
    """Собирает словарь сводных данных по Заказу.

    :param order: экземпляр Заказа.
    """
    return {
        'date_time': order.date_time.strftime('%d %B %Y, %H:%M'),
        'receiver': f'{order.user.last_name} {order.user.first_name} {order.user.profile.patronymic or ""}',
        'phone': order.user.profile.phone_number_formatted,
        'email': order.user.email,
        'total_sum': None,
        'city': order.city,
        'address': order.address,
        'delivery_method': order.delivery.name,
        'payment_method': order.payment.name,
        'bank_account': order.bank_account,
    }


def complete_order(session: str, user: User, order: Orders) -> Tuple[Orders, List[OrderItems]]:
    """Сохраняет позиции Заказа, подсчитывает общую сумму
    заказа, помещает ее в экземпляр order. Возвращает измененный
    order и созданные экземпляры OrderItems, помечает Заказ
    как "Подтвержденный" (confirmed = True).

    :param session: Идентификатор сессии.
    :param user: экземпляр авторизованного пользователя.
    :param order: экземпляр Заказа.
    """
    items = list()

    with transaction.atomic():
        total_sum = 0
        for basket_item in Basket.objects.user_basket(session_id=session, user_id=user.id):
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
