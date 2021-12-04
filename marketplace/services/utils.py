from functools import lru_cache

import transliterate
from django.apps import apps
from django.core.handlers.wsgi import WSGIRequest
from django.utils.text import slugify as django_slugify


def slugify(text):
    return transliterate.slugify(text) or django_slugify(text)


def get_username_or_session_key(request: WSGIRequest) -> str:
    """Return username, if user is authorized, and
    session key, if not.

    :param request: HTTP-request instance.
    :return: Username or session key.
    """
    return request.user.username if request.user.is_authenticated else request.session.session_key


@lru_cache(maxsize=None)
def get_model_verbose_name(app_label: str, model_name: str) -> str:
    """Возвращает verbose_name модели.

    :param app_label: Имя приложения.
    :param model_name: Имя модели.
    """
    model = apps.get_model(app_label=app_label, model_name=model_name)
    return model._meta.verbose_name
