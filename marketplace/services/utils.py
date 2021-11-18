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


def update_instance_from_form(form, instance, fields: list):
    """Обновляет значения полей экземпляра instance,
    перечисленных в fields, значениями clean_data
    формы form.

    :param form: Экземпляр заполненной формы.
    :param instance: Экземпляр модели данных для обновления.
    :param fields: Список полей, которые нужно обновить.
    :return: Измененный экземпляр модели данных.
    """
    fields_changed = [field for field in form.changed_data if field in fields]
    if fields_changed:
        list(map(lambda field: setattr(instance, field, form.cleaned_data[field]), fields_changed))
        instance.save(force_update=True, update_fields=fields_changed)
    return instance
