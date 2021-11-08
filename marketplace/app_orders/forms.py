from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from app_orders.models import (
    DeliveryMethods,
    PaymentMethods,
)


class OrderStep1AuthorizedForm(forms.ModelForm):
    patronymic = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


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


class OrderConfirmationForm(forms.Form):
    comment = forms.CharField(label=_('Comment'), max_length=255, widget=forms.Textarea())
