# fmt: off
import datetime

from app_orders.models import Orders
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView
from profiles.forms import ChangeInfoForm, RegisterForm
from profiles.models import Profile
from services.auth import registration
from services.basket import merge_baskets
from services.orders import get_user_orders
from services.view_history import get_goods_in_view_history

# fmt: on


class AccountView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = "profiles/account.html"
    context_object_name = "account"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        context["orders"] = get_user_orders(user=self.request.user, limit=3)
        start_date = datetime.datetime.now() - datetime.timedelta(days=30)
        context["view_history"] = get_goods_in_view_history(
            user=self.request.user,
            start_date=start_date,
            end_date=datetime.datetime.now(),
            limit=3,
        )
        return context


class UpdateProfile(LoginRequiredMixin, generic.UpdateView):
    form_class = ChangeInfoForm
    template_name = "profiles/profile.html"
    context_object_name = "profile"
    success_url = reverse_lazy("profile")

    def get_initial(self):
        obj = self.get_object()
        initial = super().get_initial()
        initial.update(
            {
                "phone": obj.profile.phone_number,
                "avatar": obj.profile.avatar,
                "patronymic": obj.profile.patronymic,
            }
        )
        return initial

    def get_object(self, queryset=None):
        return self.request.user


class ClientLoginView(LoginView):
    template_name = "profiles/base_login_form.html"

    def form_valid(self, form):
        old_session_key = self.request.session.session_key
        response = super().form_valid(form=form)
        new_session_key = self.request.session.session_key
        merge_baskets(
            old_session=old_session_key,
            new_session=new_session_key,
            user=self.request.user,
        )
        return response


class RegistrationView(generic.FormView):
    form_class = RegisterForm
    template_name = "profiles/base_registration.html"
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        registration(request=self.request, registration_form=self.get_form())
        return super().form_valid(form=form)


class ViewsHistoryView(ListView):
    template_name = "profiles/historyview.html"
    context_object_name = "viewed_products"

    def get_queryset(self):
        start_date = datetime.datetime.now() - datetime.timedelta(days=30)
        queryset = get_goods_in_view_history(
            user=self.request.user,
            start_date=start_date,
            end_date=datetime.datetime.now(),
        )
        return queryset


class OrdersHistoryView(ListView):
    template_name = "profiles/historyorder.html"
    model = Orders
    context_object_name = "orders"

    def get_queryset(self):
        queryset = get_user_orders(user=self.request.user, limit=None)
        return queryset
