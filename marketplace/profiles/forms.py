from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import UserAddress


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text=_("Name"))
    last_name = forms.CharField(max_length=30, help_text=_("Last Name"))
    mail = forms.CharField(max_length=30, help_text=_("Mail"))
    phone = forms.CharField(max_length=30, help_text=_("Phone"))
    patronymic = forms.CharField(max_length=30, help_text=_("Patronymic"))
    avatar = forms.ImageField(required=False, help_text=_("Avatar"))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]


class ChangeInfo(forms.ModelForm):
    mail = forms.CharField(max_length=30, help_text=_("Mail"))
    phone = forms.CharField(max_length=30, help_text=_("Phone"))
    avatar = forms.ImageField(required=False, help_text=_("Avatar"))

    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress()
        fields = ["country", "town", "region", "street", "apartment"]
