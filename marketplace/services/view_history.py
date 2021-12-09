import datetime

from loguru import logger
from profiles.models import ViewHistory


def add_goods_to_view_history(user, goods):
    """
    Function to used to add goods to view history
    """
    try:
        view_history = ViewHistory.objects.get(user=user, goods=goods)
        view_history.viewed_at = datetime.datetime.now()
        view_history.save()
    except ViewHistory.DoesNotExist:
        ViewHistory.objects.create(
            user=user, goods=goods, viewed_at=datetime.datetime.now()
        )


def delete_goods_from_view_history(user, goods):
    """
    Function to used to delete goods from view history
    """
    try:
        view_history = ViewHistory.objects.get(user=user, goods=goods)
        view_history.delete()
    except ViewHistory.DoesNotExist:
        logger.exception(
            f"Товара {goods} нет в истории просмотров пользователя - {user.username}"
        )


def is_goods_in_view_history(user, goods):
    """
    Function to used to check that goods in view history
    """
    try:
        ViewHistory.objects.get(user=user, goods=goods)
        return True
    except ViewHistory.DoesNotExist:
        logger.debug(
            f"Товара {goods} нет в истории просмотров пользователя - {user.username}"
        )
        return False


def get_goods_in_view_history(user, start_date, end_date, limit=20):
    """
    :user: UserObject
    :start_date: datetime
    :end_date: datetime
    :end_date: int
    Function to used to get goods from user view history
    :return: list[GooodsObject(1), GoodsObject(2), ...]
    """
    views_queryset = ViewHistory.objects.filter(user=user)
    if start_date:
        views_queryset = views_queryset.filter(viewed_at__gte=start_date)
    if end_date:
        views_queryset = views_queryset.filter(viewed_at__lte=end_date)
    if limit:
        views_queryset = views_queryset.order_by("-viewed_at")[:limit]
    viewed_goods = [view_history.goods for view_history in views_queryset]
    return viewed_goods


def get_goods_quantity_in_view_history(user, start_date, end_date):
    """
    :user: UserObject
    :start_date: datetime
    :end_date: datetime
    Function to used to get goods quantity in user view history
    :return: int
    """
    views_queryset = ViewHistory.objects.filter(user=user)
    if start_date:
        views_queryset = views_queryset.filter(viewed_at__gte=start_date)
    if end_date:
        views_queryset = views_queryset.filter(viewed_at__lte=end_date)
    return views_queryset.count()
