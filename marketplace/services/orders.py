from app_orders.models import Orders


def get_user_orders(user, limit):
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


def is_not_confirmed_order(user) -> bool:
    """Возвращает наличие у пользователя user незавершенного заказа."""
    return bool(Orders.objects.not_confirmed_order(user=user))


def is_not_payed_order(user) -> bool:
    """Возвращает наличие у пользователя user неоплаченного заказа."""
    return bool(Orders.objects.not_payed_orders(user=user))
