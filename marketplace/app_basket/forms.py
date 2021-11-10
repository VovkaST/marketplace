from django import forms
from django.utils.translation import gettext_lazy as _

from app_basket.models import Basket
from services.basket import is_enough_shop_balances


class PurchasePerformForm(forms.Form):
    basket_purchase = forms.Field(widget=forms.HiddenInput(), required=False)

    def is_valid(self, *args, **kwargs):
        request = kwargs.get('request')
        basket = Basket.objects.user_basket(request)
        if request:
            if request.basket_total_sum >= request.user.balance:
                self.add_error(
                    '__all__',
                    _('Not enough balances! Top up your balance or remove some items from basket.')
                )
        if basket:
            if not is_enough_shop_balances(basket):
                self.add_error(
                    '__all__',
                    _('Not enough balances of good`s in shop!')
                )
        return super().is_valid()
