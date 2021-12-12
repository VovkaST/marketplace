from django import forms
from django.conf import settings
from django.utils.translation import gettext as _


class SettingsForm(forms.Form):
    pass


def get_cache_choices():
    caches = settings.CACHES or {}
    return [(key, f"{key} ({cache['BACKEND']}") for key, cache in caches.items()]


class ClearCacheForm(forms.Form):
    cache_name = forms.ChoiceField(choices=get_cache_choices)


class GenerateBalancesForm(forms.Form):
    single_choice = forms.ChoiceField(
        choices=((1, "None"), (2, "Good"), (3, "Seller")),
        label=_("I want only one ... for balances"),
    )
    balances_quantity = forms.IntegerField(
        max_value=100, min_value=1, label=_("Quantity of different balances")
    )


class GenerateGoodsForm(forms.Form):
    quantity = forms.IntegerField(
        max_value=100, min_value=1, label=_("Quantity of different goods")
    )


class GenerateSellersForm(forms.Form):
    quantity = forms.IntegerField(
        max_value=100, min_value=1, label=_("Quantity of different sellers")
    )
