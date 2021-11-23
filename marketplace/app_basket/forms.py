from django import forms

from django.forms import Select
from django.urls import reverse_lazy

from services.sellers import get_choices_sellers_by_good


class SellerForm(forms.Form):
    seller = forms.ChoiceField(
        widget=Select(
            attrs={
                'class': 'basket-item__seller',
                'url': reverse_lazy('basket_patch_item_seller')
            }
        )
    )
    reservation_id = forms.CharField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1,
        max_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'basket-item__quantity',
                'url': reverse_lazy('basket_patch_item_quantity')
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        good_id = self.initial['good_id']
        self.fields['seller'].choices = get_choices_sellers_by_good(good=good_id)
        self.fields['quantity'].widget.attrs.update({'max': self.initial['max_quantity']})
        pass


class BasketBaseFormSet(forms.BaseFormSet):
    pass


BasketFormSet = forms.formset_factory(
    form=SellerForm, formset=BasketBaseFormSet, min_num=1, extra=0, can_delete=True, validate_min=True
)