from django import forms


class ComparisonForm(forms.Form):
    good_id = forms.CharField(widget=forms.HiddenInput())
