from django.db import models
from django.utils.translation import gettext as _


class Sellers(models.Model):
    name = models.CharField(_('Seller name'), max_length=254)
    address = models.CharField(_('Address'), max_length=254)
    email = models.EmailField(_('E-mail address'), max_length=255)
    phone = models.CharField(_('Phone number'), max_length=16)
    image = models.ImageField(_('Image (avatar)'), upload_to='files/sellers/', blank=True)
    description = models.CharField(_('Description'), max_length=1000)

    class Meta:
        db_table = 'mp_sellers'
        verbose_name = _('Seller')
        verbose_name_plural = _('Sellers')

    def __str__(self):
        if self.address:
            return f'{self.name} ({self.address})'
        return self.name


class Goods(models.Model):
    name = models.CharField(_('Good`s name'), max_length=255)
    category = models.ForeignKey(
        'GoodsCategories', verbose_name='Good category', on_delete=models.CASCADE, related_name='good_category'
    )
    limited = models.BooleanField(_('Limited edition'), default=False)
    sales = models.IntegerField(_('Sales quantity'), default=0)
    rating_average = models.IntegerField(_('Average rating value'), default=1)
    rating_total = models.IntegerField(_('Total rating value'), default=0)
    deleted = models.BooleanField(_('Deletion mark'), default=False)

    class Meta:
        db_table = 'mp_goods'
        verbose_name = _('Good item')
        verbose_name_plural = _('Good items')

    def __str__(self):
        return self.name
