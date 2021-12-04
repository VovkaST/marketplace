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


# class GoodsQuerySet(SoftDeleter):
# class GoodsQuerySet(models.QuerySet):
#     def annotate_with_reviews_count(self):
#         return self.annotate(
#             reviews_count=Count('good_balance'),
#         )
