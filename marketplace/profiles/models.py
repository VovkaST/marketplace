import re

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """Модель профиля

    :param user: Стандартная модель из коробки.
    - Lirst_name, Last_name, Email
    :param avatar: Аватар.
    :param patronymic: Отчество.
    :param phone_number: Телефон.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", verbose_name=_("User")
    )
    avatar = models.ImageField(upload_to="files/", blank=True, null=True, verbose_name=_("Avatar"))
    patronymic = models.CharField(
        max_length=150, blank=True, null=True, verbose_name=_("Patronymic")
    )
    phone_number = models.CharField(max_length=17, verbose_name=_("Phone"))

    class Meta:
        verbose_name_plural = _("Profiles")
        verbose_name = _("Profile")

    def __str__(self):
        return f"{self.user}, {self.phone_number}, {self.patronymic}"

    @property
    def phone_number_formatted(self):
        """Регулярное выражение для проверки мобильного телефона"""
        phone = re.findall(pattern=r'(\d{3})(\d{3})(\d{2})(\d{2})', string=self.phone_number)
        return '+7 ({0}) {1}-{2}-{3}'.format(*phone[0]) if phone else self.phone_number


class UserAddress(models.Model):
    """Модель профиля
        :param user: Профиль.
        :param country: Город.
        :param region: Регион.
        :param street: Улица.
        :param apartment: Квартира.
        """
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


class ViewHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="view_history",
        verbose_name=_("User"),
    )
    goods = models.ForeignKey(
        "app_sellers.Goods",
        on_delete=models.CASCADE,
        related_name="views_history",
        verbose_name=_("Goods"),
    )
    viewed_at = models.DateTimeField(_("Viewed at"), auto_now_add=True)
    compare = models.BooleanField(_("Compare"), default=False)

    class Meta:
        verbose_name = _("View history")
        verbose_name_plural = _("Views history")

    def __str__(self):
        return f"{self.user}, {self.goods}, {self.viewed_at}"
