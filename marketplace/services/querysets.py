from django.db import models


class SoftDeleter(models.QuerySet):
    def actual(self):
        return self.filter(deleted=False)

    def delete(self):
        self.update(deleted=True)

    def recover(self):
        self.update(deleted=False)


class BasketQuerySet(models.QuerySet):
    def user_basket(self, session_id: str = None, user_id: int = None):
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
        return self.filter(user_id=user_id).delete()


class OrdersQuerySet(SoftDeleter):
    def user_order(self, user):
        return self.filter(user=user)

    def incomplete_order(self, user, related=False):
        queryset = self.user_order(user=user).filter(confirmed=False)
        if related:
            queryset.select_related('delivery', 'payment', 'user')
        return queryset.first()
