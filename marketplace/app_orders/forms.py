from app_orders.models import DeliveryMethods, PaymentMethods
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from services.auth import is_user_exists


class OrderStep1AuthorizedForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-input'}))
    patronymic = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    phone_number = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "patronymic", "email", "phone_number"]

    def is_valid(self):
        super().is_valid()
        if is_user_exists(email=self.cleaned_data["email"]):
            self.add_error("email", _("User with such email address already exists."))
        return super().is_valid()


class OrderStep1NotAuthorizedForm(OrderStep1AuthorizedForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-input'}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-input'}),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-input'

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class OrderStep2Form(forms.Form):
    delivery = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=DeliveryMethods.objects.all())
    city = forms.CharField(label=_("City"), max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}))
    address = forms.CharField(label=_("Address"), max_length=1000, widget=forms.TextInput(attrs={'class': 'form-input'}))


class OrderStep3Form(forms.Form):
    payment = forms.ModelChoiceField(
        queryset=PaymentMethods.objects.all(),
        widget=forms.RadioSelect
    )


class OrderConfirmationForm(forms.Form):
    comment = forms.CharField(
        label=_("Comment"), max_length=255, required=False,
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'order-comment'})
    )


class OrderPaymentForm(forms.Form):
    bank_account = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "style": "background-color: #f9fafc; border: none; margin: auto;",
                "class": "form-input Payment-bill",
            }
        ),
        max_length=20,
    )
