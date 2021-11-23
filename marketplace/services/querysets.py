from django.db import models

from app_orders.models import Orders


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

    def incomplete_order(self, user, related=False) -> Orders:
        """Фильтр получения экземпляра незавершенного
        Заказа пользователя user.

        :param user: экземпляр авторизованного пользователя.
        :param related: Флаг необходимости предварительной
        обработки связанных объектов ('delivery', 'payment', 'user').
        """
        queryset = self.user_order(user=user).filter(confirmed=False)
        if related:
            queryset.select_related('delivery', 'payment', 'user')
        return queryset.first()
