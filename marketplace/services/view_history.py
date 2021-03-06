from django.utils import timezone
from loguru import logger

from app_sellers.models import Goods
from profiles.models import ViewHistory


def add_goods_to_view_history(user, goods):
    """
    Function to used to add goods to view history
    """
    filters = {
        'user': user,
        'goods': goods,
    }
    defaults = {
        'viewed_at': timezone.now()
    }
    ViewHistory.objects.get_or_create(defaults=defaults, **filters)


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
    :limit: int
    Function to used to get goods from user view history
    :return: list[GooodsObject(1), GoodsObject(2), ...]
    """
    views_queryset = Goods.objects.filter(views_history__user=user)
    if start_date:
        views_queryset = views_queryset.filter(views_history__viewed_at__gte=start_date)
    if end_date:
        views_queryset = views_queryset.filter(views_history__viewed_at__lte=end_date)
    if limit:
        views_queryset = views_queryset.order_by("-views_history__viewed_at")[:limit]
    return views_queryset


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
