from django.db import models


class SoftDeleter(models.QuerySet):
    def actual(self):
        return self.filter(deleted=False)

    def delete(self):
        self.update(deleted=True)

    def recover(self):
        self.update(deleted=False)


class BasketQuerySet(models.QuerySet):
    def user_basket(self, request):
        if request.user.is_authenticated:
            filters = {'user': request.user}
        else:
            filters = {'session': request.session.session_key}
        return self.filter(**filters)
