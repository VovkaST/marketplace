from django import forms
from django.utils.translation import gettext_lazy as _

from app_import.models import ImportProtocol


MODELS_CHOICES = [
    ('', '', ),
    ('sellers', _('Sellers'), ),
    ('goods', _('Goods'), ),
]


class ImportForm(forms.ModelForm):
    target_model = forms.ChoiceField(choices=MODELS_CHOICES)
    update_data = forms.BooleanField(required=False)

    class Meta:
        model = ImportProtocol
        fields = ['filename', 'target_model', 'update_data']
