from django import forms
from django.conf import settings


class SettingsForm(forms.Form):
    pass


def get_cache_choices():
    caches = settings.CACHES or {}
    return [(key, f"{key} ({cache['BACKEND']}") for key, cache in caches.items()]


class ClearCacheForm(forms.Form):
    cache_name = forms.ChoiceField(choices=get_cache_choices)
