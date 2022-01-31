from django import forms

from django.forms import Select
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from services.basket import is_enough_shop_balances
from services.sellers import get_choices_sellers_by_good


class SellerForm(forms.Form):
    seller = forms.ChoiceField(
        widget=Select(
            attrs={
                'class': 'basket-item__seller form-select',
                'url': reverse_lazy('basket_patch_item_seller')
            }
        )
    )
    reservation_id = forms.CharField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.TextInput(
            attrs={
                'class': 'basket-item__quantity Amount-input form-input',
                'url': reverse_lazy('basket_patch_item_quantity')
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        good_id = self.initial.get('good_id')
        if good_id is not None:
            self.fields['seller'].choices = get_choices_sellers_by_good(good=good_id)
            self.fields['quantity'].widget.attrs.update({'max': self.initial['max_quantity']})


class BasketBaseFormSet(forms.BaseFormSet):
    def clean(self):
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            reservation_id = form.cleaned_data.get('reservation_id')
            needle_quantity = form.cleaned_data.get('quantity')
            if not is_enough_shop_balances(reservation_id, needle_quantity):
                form.add_error('__all__', _('Not enough balances.'))


BasketFormSet = forms.formset_factory(
    form=SellerForm, formset=BasketBaseFormSet, min_num=1, extra=0, can_delete=True, validate_min=True
)
