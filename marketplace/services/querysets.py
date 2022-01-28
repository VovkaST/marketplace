from typing import List

from django.db import models
from django.db.models import Q


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


class GoodsQuerySet(SoftDeleter):
    def existing(self):
        """Товары, связанные с балансом продавца."""
        return self.filter(good_balance__isnull=False).distinct()

    def in_category(self, category_id):
        """Товары из категории category_id."""
        return self.existing().filter(category=category_id)


class BasketQuerySet(models.QuerySet):
    """QuerySet Корзины"""

    def user_basket(self, session_id: str = None, user_id: int = None):
        """Фильтр получения Корзины пользователя по его идентификатору
        (user_id), имени сессии (session_id).

        :param session_id: Имя сессии.
        :param user_id: Идентификатор пользователя.
        """
        if user_id:
            return self.filter(user_id=user_id)
        return self.filter(session=session_id)

    def delete_user_basket(self, user_id: int):
        """Удаление Корзины пользователя.

        :param user_id: Идентификатор пользователя.
        """
        return self.filter(user_id=user_id).delete()


class ComparisonQuerySet(models.QuerySet):
    def user_comparison(self, session: str, user_id: int = None):
        """Список товаров к сравнению пользователя user_id.

        :param user_id: Идентификатор пользователя.
        :param session: Имя сессии.
        """
        if user_id:
            return self.filter(user_id=user_id)
        return self.filter(session=session)

    def delete_user_comparison(self, session: str, user_id: int):
        """Удаление списка сравнения пользователя.

        :param user_id: Идентификатор пользователя.
        :param session: Имя сессии.
        """
        return self.filter(Q(user_id=user_id) | Q(session=session)).delete()

    def delete_good_comparison(self, good_id: int, session: str, user_id: int):
        """Удаление списка сравнения пользователя.

        :param good_id: Идентификатор товара.
        :param user_id: Идентификатор пользователя.
        :param session: Имя сессии.
        """
        return self.filter(Q(good_id=good_id), Q(user_id=user_id) | Q(session=session)).delete()


class OrdersQuerySet(SoftDeleter):
    """QuerySet Заказов"""

    def user_order(self, user):
        """Фильтр получения Заказов пользователя user.

        :param user: экземпляр авторизованного пользователя.
        """
        return self.filter(user=user)

    def not_confirmed_order(self, user, related=False):
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

    def not_payed_orders(self, user, related=False):
        if user.is_anonymous:
            return self.model.objects.none()

        queryset = self.user_order(user=user).filter(confirmed=True, payment_state=False)
        if related:
            queryset.select_related('delivery', 'payment', 'user')
        return queryset


class SellerQuerySet(models.QuerySet):
    def by_good(self, good: int, only_available: bool = True):
        """Фильтр продавцов по товару.

        :param good: Целевой товар.
        :param only_available: Флаг необходимости фильтрации только
        тех продавцов, у которых товар good есть в наличии.
        """
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
        """Фильтр заданий пользователя."""
        return self.filter(~Q(task_id=''), user=user)

    def tasks_results(self, user, tasks: List[str]):
        """Получение результатов выполнения задания по их id."""
        values = ['task_id', 'is_imported', 'total_objects', 'new_objects', 'updated_objects']
        return self.active_tasks(user=user).filter(task_id__in=tasks).values(*values)
