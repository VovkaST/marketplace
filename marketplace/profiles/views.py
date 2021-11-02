from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from profiles.forms import ChangeInfoForm, RegisterForm
from profiles.models import Profile


class AccountView(generic.DetailView):
    model = Profile
    template_name = "profiles/account.html"
    context_object_name = "account"

    def get_object(self, queryset=None):
        return self.request.user


class UpdateProfile(generic.UpdateView):
    form_class = ChangeInfoForm
    template_name = "profiles/profile.html"
    context_object_name = "profile"
    success_url = reverse_lazy('profile')

    def get_initial(self):
        obj = self.get_object()
        initial = super().get_initial()
        initial.update({
            'phone': obj.profile.phone_number,
            'avatar': obj.profile.avatar,
        })
        return initial

    def get_object(self, queryset=None):
        return self.request.user


class ClientLoginView(LoginView):
    template_name = "profiles/base_login_form.html"


class RegistrationView(generic.FormView):
    form_class = RegisterForm

    def form_valid(self, form):
        Profile.objects.create(**{
            'user': form.save(),
            'phone_number': form.cleaned_data.get("phone"),
            'avatar': form.cleaned_data.get("avatar"),
            'patronymic': form.cleaned_data.get("patronymic"),
        })
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form=form)
