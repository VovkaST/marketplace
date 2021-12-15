from django import forms
from django.utils.translation import gettext_lazy as _

from app_import.models import ImportProtocol
from services.utils import get_model_verbose_name


MODELS_CHOICES = [
    ('', '', ),
    ('sellers', get_model_verbose_name(app_label='app_sellers', model_name='Sellers'), ),
    ('goods', get_model_verbose_name(app_label='app_sellers', model_name='Goods'), ),
    ('goods_descriptions', get_model_verbose_name(app_label='app_sellers', model_name='GoodsDescriptionsValues'), ),
]


class ImportForm(forms.ModelForm):
    target_model = forms.ChoiceField(choices=MODELS_CHOICES)
    update_data = forms.BooleanField(required=False)
    delimiter = forms.CharField(max_length=1, initial=';')

    class Meta:
        model = ImportProtocol
        fields = ['filename', 'target_model', 'update_data']

