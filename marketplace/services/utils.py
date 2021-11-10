import transliterate
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
