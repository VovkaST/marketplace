from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from profiles.forms import (
    ChangeInfoForm,
    RegisterForm,
)
from profiles.models import Profile
from services.auth import registration
from services.basket import merge_baskets


class AccountView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = "profiles/account.html"
    context_object_name = "account"

    def get_object(self, queryset=None):
        return self.request.user


class UpdateProfile(LoginRequiredMixin, generic.UpdateView):
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

    def form_valid(self, form):
        old_session_key = self.request.session.session_key
        response = super().form_valid(form=form)
        new_session_key = self.request.session.session_key
        merge_baskets(old_session=old_session_key, new_session=new_session_key, user=self.request.user)
        return response


class RegistrationView(generic.FormView):
    form_class = RegisterForm

    def form_valid(self, form):
        registration(request=self.request, registration_form=self.get_form())
        return super().form_valid(form=form)
