from django.db import models


class SoftDeleter(models.QuerySet):
    def actual(self):
        return self.filter(deleted=False)

    def delete(self):
        self.update(deleted=True)

    def recover(self):
        self.update(deleted=False)


# class GoodsQuerySet(SoftDeleter):
# class GoodsQuerySet(models.QuerySet):
#     def annotate_with_reviews_count(self):
#         return self.annotate(
#             reviews_count=Count('good_balance'),
#         )
