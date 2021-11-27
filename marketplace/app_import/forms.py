from django import forms

from app_import.models import ImportProtocol


class ImportForm(forms.ModelForm):
    class Meta:
        model = ImportProtocol
        fields = ['filename']
