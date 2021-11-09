from django.db import models


class SoftDeleter(models.QuerySet):
    def actual(self):
        return self.filter(deleted=False)

    def delete(self):
        self.update(deleted=True)

    def recover(self):
        self.update(deleted=False)


class OrdersQuerySet(SoftDeleter):
    def user_order(self, user):
        return self.filter(user=user)

    def incomplete_order(self, user, related=False):
        queryset = self.user_order(user=user).filter(payment_state=False)
        if related:
            queryset.select_related('delivery', 'payment', 'user')
        return queryset.first()
