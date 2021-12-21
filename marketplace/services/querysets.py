from typing import List

from django.db import models
from django.db.models import Q

from loguru import logger


class SoftDeleter(models.QuerySet):
    """QuerySet мягкого удаления объектов"""

    def actual(self):
        """Фильтр получения объектов, не помеченных как удаленные."""
        return self.filter(deleted=False)

    def delete(self):
        """Пометить объект как удаленный."""
        self.update(deleted=True)

    def recover(self):
        """Восстановить объект (снять отметку об удалении)."""
        self.update(deleted=False)


class BasketQuerySet(models.QuerySet):
    """QuerySet Корзины"""

    def user_basket(self, session_id: str = None, user_id: int = None):
        """Фильтр получения Корзины пользователя по его идентификатору
        (user_id), имени сессии (session_id) или их связке.

        :param session_id: Имя сессии.
        :param user_id: Идентификатор пользователя.
        """
        if all([user_id, session_id]):
            filters = {
                'user_id': user_id,
                'session': session_id,
            }
        elif user_id:
            filters = {'user_id': user_id}
        else:
            filters = {'session': session_id}
        return self.filter(**filters)

    def delete_user_basket(self, user_id: int):
        """Удаление Корзины пользователя.

        :param user_id: Идентификатор пользователя.
        """
        return self.filter(user_id=user_id).delete()


class OrdersQuerySet(SoftDeleter):
    """QuerySet Заказов"""

    def user_order(self, user):
        """Фильтр получения Заказов пользователя user.

        :param user: экземпляр авторизованного пользователя.
        """
        return self.filter(user=user)

    def incomplete_order(self, user, related=False):
        """Фильтр получения экземпляра незавершенного
        Заказа пользователя user.

        :param user: экземпляр авторизованного пользователя.
        :param related: Флаг необходимости предварительной
        обработки связанных объектов ('delivery', 'payment', 'user').
        """
        if user.is_anonymous:
            return self.model.objects.none()

        queryset = self.user_order(user=user).filter(confirmed=False)
        if related:
            queryset.select_related('delivery', 'payment', 'user')
        return queryset.first()


class SellerQuerySet(models.QuerySet):
    def by_good(self, good, only_available=True):
        filters = dict()
        if isinstance(good, int):
            filters.update({'balance_owner__good_id': good})
        else:
            filters.update({'balance_owner__good': good})
        if only_available:
            filters.update({'balance_owner__quantity__gt': 0})
        return self.filter(**filters)

    def get_by_natural_key(self, *, slug):
        return self.filter(slug=slug).first()


class ImportProtocolQuerySet(models.QuerySet):
    def active_tasks(self, user):
        return self.filter(~Q(task_id=''), user=user)

    def tasks_results(self, user, tasks: List[str]):
        values = ['task_id', 'is_imported', 'total_objects', 'new_objects', 'updated_objects']
        return self.active_tasks(user=user).filter(task_id__in=tasks).values(*values)


# class GoodsQuerySet(SoftDeleter):
# class GoodsQuerySet(models.QuerySet):
#     def annotate_with_reviews_count(self):
#         return self.annotate(
#             reviews_count=Count('good_balance'),
#         )
