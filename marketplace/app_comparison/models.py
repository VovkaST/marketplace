from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from app_sellers.models import Goods
from services.querysets import ComparisonQuerySet


class Comparison(models.Model):
    """Сравнение товаров"""

    user = models.ForeignKey(
        User, verbose_name=_('User'), related_name='user_comparison', on_delete=models.CASCADE, null=True, blank=True
    )
    session = models.CharField(_('Session id'), max_length=32)
    good = models.ForeignKey(
        Goods, on_delete=models.CASCADE, related_name='good_item', verbose_name=_('Good item')
    )
    modified_at = models.DateTimeField(_('Modifying date, time'), editable=False, auto_now=True)

    objects = ComparisonQuerySet.as_manager()

    def __str__(self):
        return self.user.username if self.user else self.session

    class Meta:
        db_table = 'mp_comparison'
        verbose_name = _('Comparison')
        verbose_name_plural = _('Comparison')
        indexes = [
            models.Index(fields=['session'], name='idx_session_comparison'),
        ]
        unique_together = ['session', 'good']
