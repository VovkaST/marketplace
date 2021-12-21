import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import UserAddress


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text=_("Name"))
    last_name = forms.CharField(max_length=30, help_text=_("Last Name"))
    mail = forms.CharField(max_length=30, help_text=_("Mail"))
    phone_number = forms.CharField(max_length=30, help_text=_("Phone number"))
    patronymic = forms.CharField(
        max_length=30, help_text=_("Patronymic"), required=False
    )
    avatar = forms.ImageField(required=False, help_text=_("Avatar"))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]


class ChangeInfoForm(forms.ModelForm):
    patronymic = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=30)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_phone(self):
        phone = re.sub(r"\D", "", self.cleaned_data["phone"])
        if len(phone) != 11:
            raise ValidationError(_("Invalid phone format"), code="invalid")
        return phone[1:]

    def save(self, commit=True):
        super().save(commit=commit)
        self.instance.profile.patronymic = self.cleaned_data["patronymic"]
        self.instance.profile.phone_number = self.cleaned_data["phone"]
        self.instance.profile.avatar = self.cleaned_data["avatar"]
        self.instance.profile.save()
        return self.instance


class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress()
        fields = ["country", "town", "region", "street", "apartment"]
