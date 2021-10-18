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
