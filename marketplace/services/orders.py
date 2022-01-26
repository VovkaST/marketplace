from app_orders.models import OrderItems, Orders
from app_sellers.models import Balances
from django.contrib.auth.models import User
from loguru import logger


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
