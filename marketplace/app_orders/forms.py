from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from app_orders.models import (
    DeliveryMethods,
    PaymentMethods,
)
from services.auth import is_user_exists


class OrderStep1AuthorizedForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    patronymic = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "patronymic", "email", "phone_number"]

    def is_valid(self):
        super().is_valid()
        if not is_user_exists(email=self.cleaned_data['email']):
            self.add_error('email', _('User with such email address already exists.'))
        return super().is_valid()


class OrderStep1NotAuthorizedForm(OrderStep1AuthorizedForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        # help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        # help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]


class OrderStep2Form(forms.Form):
    delivery = forms.ModelChoiceField(queryset=DeliveryMethods.objects.all())
    city = forms.CharField(label=_('City'), max_length=255)
    address = forms.CharField(label=_('Address'), max_length=1000)


class OrderStep3Form(forms.Form):
    payment = forms.ModelChoiceField(queryset=PaymentMethods.objects.all())
    bank_account = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                'maxlength': 20,
            }),
        max_length=20
    )


class OrderConfirmationForm(forms.Form):
    comment = forms.CharField(label=_('Comment'), max_length=255, widget=forms.Textarea())
