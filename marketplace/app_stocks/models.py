from django.db import models
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _


class StockType(models.Model):
    """Model of stock type (vocabulary). Represents stock
    on single good, goods set, basket or etc."""

    name = models.CharField(_('Name'), max_length=255)

    class Meta:
        db_table = 'mp_stock_types'
        verbose_name = _('Stock type')
        verbose_name_plural = _('Stock types')

    def __str__(self):
        return self.name


class StockMethod(models.Model):
    """Model of stock methods (vocabulary). Contains
    stock`s methods: percent, fixed stock sum or fixed
    final sum."""

    name = models.CharField(_('Name'), max_length=255)

    class Meta:
        db_table = 'mp_stock_methods'
        verbose_name = _('Stock method')
        verbose_name_plural = _('Stock methods')

    def __str__(self):
        return self.name


class Stocks(models.Model):
    """Main model of marketplace stocks"""

    type = models.ForeignKey(
        StockType, verbose_name=_('Stock type'), on_delete=models.CASCADE, related_name='stock_type'
    )
    title = models.CharField(_('Stock title'), max_length=255)
    context = models.CharField(_('Stock context'), max_length=255)
    method = models.ForeignKey(
        StockMethod, verbose_name=_('Stock method'), on_delete=models.CASCADE, related_name='stock_method'
    )
    amount = models.DecimalField(_('Stock amount'), decimal_places=10, max_digits=18)
    index_min = models.DecimalField(_('Min stock index'), decimal_places=10, max_digits=18)
    index_max = models.DecimalField(_('Max stock index'), decimal_places=10, max_digits=18)
    since = models.DateTimeField(default=timezone.now)
    until = models.DateTimeField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'mp_stocks'
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')

    def __str__(self):
        period = _('%(begin_date)s &ndash; %(end_date)s') % {
            'begin_date': date_format(self.since, format='SHORT_DATE_FORMAT', use_l10n=True),
            'end_date': date_format(self.until, format='SHORT_DATE_FORMAT', use_l10n=True),
        }
        return mark_safe(f'{self.title} ({period})')

