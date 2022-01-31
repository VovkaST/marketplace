from copy import copy

from django import template
from django.template.defaultfilters import stringfilter
from django.urls import reverse
from django.utils.safestring import mark_safe

from services.utils import slugify

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


@register.filter
def get(dictionary: dict, key):
    """Тэг для получения значения из словаря по ключу.
    :param dictionary: Словарь с данными.
    :param key: Имя ключа.
    """
    return dictionary.get(key, '-')


@register.filter
def get_list_item(values_list: list, index: int):
    """Тэг для получения первого элемента списка.
    :param values_list: Список значений.
    :param index: Индекс элемента.
    """
    return values_list[index]


@register.simple_tag
@stringfilter
def transliterate(string: str) -> str:
    """Тэг для транслитерации строки по принципу slug.
    :param string: Строка для преобразования.
    """
    return slugify(string)


@register.simple_tag
def rating(index: int) -> str:
    """Тэг отрисовки звезды рейтинга.
    :param index: Рейтинг в виде целого числа.
    :return: HTML-строка рейтинга товара.
    """
    star_html = '''
    <span class="Rating-star {star_class}">
        <svg xmlns="http://www.w3.org/2000/svg" width="19" height="18" viewBox="0 0 19 18">
            <g>
              <path fill="#ffc000" d="M9.5 14.925L3.629 18l1.121-6.512L0 6.875l6.564-.95L9.5 0l2.936 5.925 6.564.95-4.75 4.613L15.371 18z"></path>
            </g>
        </svg>
    </span>
    '''
    stars = list()
    for i in range(1, 6):
        stars.append(copy(star_html).format(star_class='Rating-star_view' if i <= index else ''))
    return mark_safe(''.join(stars))
