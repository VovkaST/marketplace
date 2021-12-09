from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.utils.translation import gettext as _


class Banner(models.Model):
    """Модель баннера"""

    title = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_("banner title")
    )
    text = models.CharField(
        max_length=256, null=True, blank=True, verbose_name=_("banner text")
    )
    image = models.FileField(
        upload_to="images/banners",
        null=True,
        blank=True,
        verbose_name=_("banner image"),
    )
    link = models.CharField(max_length=256, verbose_name=_("banner link"))
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("banner created date")
    )
    activity = models.BooleanField(default=False, verbose_name=_("banner activity"))

    class Meta:
        verbose_name = _("banner")
        verbose_name_plural = _("banners")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        key_save_banner = make_template_fragment_key("banner_cache")
        cache.delete(key_save_banner)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        key_delete_banner = make_template_fragment_key("banner_cache")
        cache.delete(key_delete_banner)


class GoodCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               related_name='sub_category',
                               verbose_name=_('Parent Category'))
    image = models.FileField(upload_to='images/categories', null=True, blank=True)
    deleted = models.BooleanField(verbose_name=_('Deleted'), default=False)
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    order_index = models.IntegerField(verbose_name=_('Order Index'))

    class Meta:
        db_table = 'mp_goods_categories'
        verbose_name = _('Good Category')
        verbose_name_plural = _('Goods Categories')

    def __str__(self):
        if not self.active:
            return f'{self.name} ({_("Not active")})'
        return self.name

    @property
    def photo_url(self):
        return self.image.url if self.image else ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        key_save_category = make_template_fragment_key("category_cache")
        cache.delete(key_save_category)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        key_delete_category = make_template_fragment_key("category_cache")
        cache.delete(key_delete_category)
