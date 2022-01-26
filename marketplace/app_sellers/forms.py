from django import forms

from .models import RatingStar, Reviews


class ReviewForm(forms.ModelForm):
    """ Форма отзыва

    :param star: оценка товара.

    """
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Reviews
        fields = ("comment", "star")
