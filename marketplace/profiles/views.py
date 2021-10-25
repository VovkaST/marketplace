from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View, generic

from .forms import ChangeInfo, RegisterForm
from .models import Profile


class AccountView(generic.ListView):
    model = Profile
    template_name = "profiles/account.html"
    context_object_name = "accounts"

    def get_object(self):
        pass


class UpdateProfile(generic.UpdateView):
    model = User
    form_class = ChangeInfo
    template_name = "profiles/profile.html"
    context_object_name = "profiles"

    def get_object(self):
        pass

    def get_absolute_url(self):
        return HttpResponseRedirect("/account/profile/")


class LoginViews(LoginView):
    template_name = "profiles/base_login_form.html"


class LogoutViews(LogoutView):
    pass


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, "profiles/base_registration.html", {"form": form})

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                mail = form.cleaned_data.get("mail")
                phone = form.cleaned_data.get("phone")
                avatar = form.cleaned_data.get("avatar")
                patronymic = form.cleaned_data.get("patronymic")
                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                Profile.objects.create(
                    user=user,
                    mail=mail,
                    phone=phone,
                    avatar=avatar,
                    patronymic=patronymic,
                    first_name=first_name,
                    last_name=last_name,
                )
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=password)
                login(request, user)
                return render(request, "profiles/account.html", {"form": form})
            else:
                form = RegisterForm()
                return render(
                    request, "profiles/base_registration.html", {"form": form}
                )
