from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user", verbose_name=_("User")
    )
    avatar = models.ImageField(upload_to="files/", blank=True, verbose_name=_("Avatar"))
    patronymic = models.CharField(
        max_length=150, blank=True, verbose_name=_("Patronymic")
    )
    phone_number = models.CharField(max_length=17, verbose_name=_("Phone"))

    class Meta:
        verbose_name_plural = _("Users")
        verbose_name = _("User")

    def __str__(self):
        return f"{self.pk}, {self.phone_number}, {self.patronymic}"


class UserAddress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="address",
        verbose_name=_("Address"),
    )
    country = models.CharField(max_length=30, verbose_name=_("Country"))
    town = models.CharField(max_length=30, verbose_name=_("Town"))
    region = models.CharField(max_length=30, blank=True, verbose_name=_("Region"))
    street = models.CharField(max_length=30, verbose_name=_("Street"))
    apartment = models.PositiveIntegerField(verbose_name=_("Apartment"))

    class Meta:
        verbose_name_plural = _("Addresses")
        verbose_name = _("Address")

    def __str__(self):
        return f"{self.country}, {self.town}, {self.region}, {self.street}, {self.apartment}"
