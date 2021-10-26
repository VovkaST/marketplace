import transliterate
from django.utils.text import slugify as django_slugify


def slugify(text):
    return transliterate.slugify(text) or django_slugify(text)
