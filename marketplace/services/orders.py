from app_orders.models import Orders


def get_user_orders(user, limit):
    """
    :user: UserObject
    :limit: int
    Function to used to get orders from user orders history
    :return: Queryset[OrderObject(1), OrderObject(2), ...]
    """
    orders_queryset = Orders.objects.filter(user=user)
    if limit:
        if orders_queryset.count() > limit:
            orders_queryset = orders_queryset[:limit]
    return orders_queryset


def is_incomplete_order(user) -> bool:
    """Возвращает наличие у пользователя user незавершенного заказа."""
    return bool(Orders.objects.incomplete_order(user=user))
