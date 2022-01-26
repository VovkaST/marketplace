from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import GoodCategory
from services.models import NaturalKeyModel
from services.querysets import GoodsQuerySet, SellerQuerySet
from services.utils import slugify


class Sellers(NaturalKeyModel, models.Model):
    slug = models.SlugField(blank=True, unique=True)
    name = models.CharField(_("Seller name"), max_length=254)
    address = models.CharField(_("Address"), max_length=254)
    email = models.EmailField(_("E-mail address"), max_length=255)
    phone = models.CharField(_("Phone number"), max_length=16)
    image = models.ImageField(
        _("Image (avatar)"), upload_to="files/sellers/", blank=True
    )
    description = models.CharField(_("Description"), max_length=1000)

    objects = SellerQuerySet.as_manager()

    def clean(self):
        self.slug = slugify(self.name)

    def natural_key(self):
        if not self.slug:
            self.clean()
        return {
            "slug": self.slug,
        }

    class Meta:
        db_table = "mp_sellers"
        verbose_name = _("Seller")
        verbose_name_plural = _("Sellers")

    def __str__(self):
        if self.address:
            return f"{self.name} ({self.address})"
        return self.name


class GoodsDescriptionsValues(NaturalKeyModel, models.Model):
    value = models.CharField(_("Description value"), max_length=254)

    feature = models.ForeignKey(
        "GoodsDescriptionsValues",
        blank=True,
        null=True,
        default=None,
        verbose_name=_("Description item"),
        on_delete=models.CASCADE,
        related_name="description_feature",
    )

    def natural_key(self):
        return {
            "id": self.id,
        }

    def __str__(self):
        if self.feature:
            return f"{self.feature.value}: {self.value}"
        return self.value

    class Meta:
        db_table = "mp_goods_descriptions_values"
        verbose_name = _("Description value")
        verbose_name_plural = _("Description values")


class Goods(models.Model):
    name = models.CharField(_("Good`s name"), max_length=255)
    category = models.ForeignKey(
        GoodCategory,
        verbose_name=_("Good category"),
        on_delete=models.CASCADE,
        related_name="good_category",
    )
    limited = models.BooleanField(_("Limited edition"), default=False)
    sales = models.IntegerField(_("Sales quantity"), default=0)
    rating_average = models.IntegerField(_("Average rating value"), default=1)
    rating_total = models.IntegerField(_("Total rating value"), default=0)
    deleted = models.BooleanField(_("Deletion mark"), default=False)
    description = models.ManyToManyField(
        GoodsDescriptionsValues,
        db_table="mp_goods_descriptions",
        related_name="good_descriptions",
    )

    objects = GoodsQuerySet.as_manager()

    class Meta:
        db_table = "mp_goods"
        verbose_name = _("Good item")
        verbose_name_plural = _("Good items")

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    good = models.ForeignKey(
        Goods,
        verbose_name=_("Goods item"),
        on_delete=models.CASCADE,
        related_name="good_images",
    )
    image = models.ImageField(upload_to="goods-images/", verbose_name=_("Image"))

    class Meta:
        db_table = "mp_goods_images"
        verbose_name = _("Goods image")
        verbose_name_plural = _("Goods images")

    def __str__(self):
        return f"{self.pk}. {self.good} image"


class Balances(models.Model):
    seller = models.ForeignKey(
        Sellers,
        verbose_name=_("Seller"),
        on_delete=models.CASCADE,
        related_name="balance_owner",
    )
    good = models.ForeignKey(
        Goods,
        verbose_name=_("Good"),
        on_delete=models.CASCADE,
        related_name="good_balance",
    )
    quantity = models.IntegerField(_("Good`s quantity"), default=0)
    price = models.DecimalField(_("Price"), decimal_places=2, max_digits=10)

    class Meta:
        db_table = "mp_balances"
        verbose_name = _("Balance")
        verbose_name_plural = _("Balances")

    def __str__(self):
        return f"{self.quantity} ({self.price})"


class RatingStar(models.Model):
    value = models.SmallIntegerField(verbose_name=_("value"), default=0)

    class Meta:
        verbose_name_plural = _("RatingStars")
        verbose_name = _("RatingStar")
        ordering = ["-value"]

    def __str__(self):
        return f"{self.value}"


class Reviews(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="user_reviews",
    )
    good_review = models.ForeignKey(
        Goods,
        verbose_name=_("Good review"),
        on_delete=models.CASCADE,
        related_name="good_review",
    )
    comment = models.TextField(verbose_name=_("Comments"))
    star = models.ForeignKey(
        RatingStar,
        verbose_name=_("star"),
        on_delete=models.CASCADE,
        related_name="star",
    )
    crated_at = models.DateTimeField(auto_now=True, verbose_name=_("Crated at"))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return f"{self.user}, {self.comment}, {self.comment}, {self.star}"
