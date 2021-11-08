from django import template
from django.template.defaultfilters import stringfilter
from django.urls import reverse

register = template.Library()


@register.filter(name='if_current_url')
@stringfilter
def if_current_url(current_url: str, expected_url_name: str) -> bool:
    """Тэг для сравнения текущего url c ожидаемым.
    :param current_url: текущий url.
    :param expected_url_name: имя ожидаемого url.
    :return: Результат сравнения.
    """
    return current_url == reverse(expected_url_name)
