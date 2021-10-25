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
    link = models.CharField(verbose_name=_("banner link"))
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
