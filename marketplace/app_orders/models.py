from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.formats import date_format, number_format
from django.utils.translation import gettext as _

from app_sellers.models import (
    Goods,
    Sellers,
)
from services.querysets import SoftDeleter


class DeliveryMethods(models.Model):
    name = models.CharField(_('Delivery name'), max_length=255)
    price = models.DecimalField(_('Delivery price'), default=0, decimal_places=2, max_digits=19)

    def __str__(self):
        if self.price:
            return f'{self.name} ({self.price})'
        return self.name

    class Meta:
        db_table = 'mp_delivery_methods'
        verbose_name = _('Delivery method')
        verbose_name_plural = _('Delivery methods')


class PaymentMethods(models.Model):
    name = models.CharField(_('Payment name'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'mp_payment_methods'
        verbose_name = _('Payment method')
        verbose_name_plural = _('Payment methods')


class Orders(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='user_orders')
    total_sum = models.DecimalField(_('Total sum'), default=0, decimal_places=2, max_digits=19)
    date_time = models.DateTimeField(_('Date, time'), default=timezone.now())
    delivery = models.ForeignKey(
        DeliveryMethods, verbose_name=_('Delivery methods'), on_delete=models.CASCADE, related_name='delivery_method'
    )
    payment = models.ForeignKey(
        PaymentMethods, verbose_name=_('Payment methods'), on_delete=models.CASCADE, related_name='payment_method'
    )
    payment_state = models.BooleanField(_('Payment state'), default=False)
    city = models.CharField(_('City'), max_length=255)
    address = models.CharField(_('Address'), max_length=1000)
    comment = models.CharField(_('Comment'), max_length=255)
    deleted = models.BooleanField(_("Deletion mark"), default=False)

    objects = SoftDeleter.as_manager()

    def __str__(self):
        return _('%(begin_date)s &ndash; %(total_sum)s. %(pay_state)s.') % {
            'begin_date': date_format(self.date_time, format='SHORT_DATE_FORMAT', use_l10n=True),
            'total_sum': number_format(self.total_sum, decimal_pos=2, use_l10n=True),
            'pay_state': _('Paid') if self.payment_state else _('Not paid')
        }

    class Meta:
        db_table = 'mp_orders'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, verbose_name=_('Order'), on_delete=models.CASCADE, related_name='order')
    seller = models.ForeignKey(Sellers, verbose_name=_('Seller'), on_delete=models.CASCADE, related_name='seller')
    good = models.ForeignKey(Goods, verbose_name=_('Good'), on_delete=models.CASCADE, related_name='good')
    quantity = models.IntegerField(_('Quantity'), default=1)
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=19)
    total_price = models.DecimalField(_('Total price'), decimal_places=2, max_digits=19)

    def __str__(self):
        return f'{self.good} &ndash; {self.quantity}x{self.price}'

    class Meta:
        db_table = 'mp_order_items'
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')
