from django.contrib.auth import authenticate, login, get_user_model
from django.core.handlers.wsgi import WSGIRequest

from profiles.forms import RegisterForm


def registration(request: WSGIRequest, registration_form: RegisterForm):
    """Процедура регистрации пользователя. После успешной
    регистрации происходит авторизация на сайте.

    :param request: экземпляр http-запроса.
    :param registration_form: валидный экземпляр формы регистрации.
    :return: Экземпляр авторизованного пользователя.
    """
    username = registration_form.cleaned_data.get("username")
    password = registration_form.cleaned_data.get("password1")

    user_instance = registration_form.save()
    user_instance.set_password(password)
    user_instance.save()

    user_instance.profile.phone_number = registration_form.cleaned_data.get("phone_number")
    user_instance.profile.avatar = registration_form.cleaned_data.get("avatar")
    user_instance.profile.patronymic = registration_form.cleaned_data.get("patronymic")
    user_instance.profile.save()

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
