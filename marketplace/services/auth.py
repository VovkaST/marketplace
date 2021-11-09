from django.contrib.auth import authenticate, login, get_user_model
from django.core.handlers.wsgi import WSGIRequest

from profiles.forms import RegisterForm
from profiles.models import Profile


def registration(request: WSGIRequest, registration_form: RegisterForm):
    """Процедура регистрации пользователя. После успешной
    регистрации происходит авторизация на сайте.

    :param request: экземпляр http-запроса.
    :param registration_form: валидный экземпляр формы регистрации.
    :return: Экземпляр авторизованного пользователя.
    """
    Profile.objects.create(**{
        'user': registration_form.save(),
        'phone_number': registration_form.cleaned_data.get("phone_number"),
        'avatar': registration_form.cleaned_data.get("avatar"),
        'patronymic': registration_form.cleaned_data.get("patronymic"),
    })
    username = registration_form.cleaned_data.get("username")
    password = registration_form.cleaned_data.get("password1")
    user = authenticate(username=username, password=password)
    login(request, user)
    return user


def is_user_exists(email: str) -> bool:
    """По адресу электронной почты проверяет существует ли
    пользователь.

    :param email: Строка с адресом электронной почты пользователя.
    """
    user_model = get_user_model()
    return user_model.objects.filter(email=email).count() != 0
