from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app_sellers.models import Balances
from services.querysets import BasketQuerySet


class Basket(models.Model):
    """User`s basket of goods"""

    user = models.ForeignKey(
        User, verbose_name=_('User'), related_name='user_basket', on_delete=models.CASCADE, null=True, blank=True
    )
    session = models.CharField(_('Session id'), max_length=32)
    reservation = models.ForeignKey(
        Balances, on_delete=models.CASCADE, related_name='reservation_item', verbose_name=_('Reservation')
    )
    quantity = models.FloatField(_('Quantity'), default=0)
    modified_at = models.DateTimeField(_('Modifying date, time'), default=timezone.now, editable=False)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return self.user.username if self.user else self.session

    class Meta:
        db_table = 'mp_basket'
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')
        indexes = [
            models.Index(fields=['session'], name='idx_session_basket'),
        ]
