from app_orders.models import Orders


def get_user_orders(user, limit=3):
    orders = Orders.objects.filter(user=user)[:limit]
    return orders
