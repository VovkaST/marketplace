from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic.base import ContextMixin

from app_orders.forms import (
    OrderConfirmationForm,
    OrderStep1AuthorizedForm,
    OrderStep1NotAuthorizedForm,
    OrderStep2Form,
    OrderStep3Form,
)
from app_orders.models import Orders
from main.views import PageInfoMixin
from services.auth import registration
from services.utils import update_instance_from_form


class OrderMixin(ContextMixin):
    """Миксин работы с Заказами и добавления данных по его этапам."""

    template_name = 'app_orders/order_create.html'
    step_name = None
    step = 1

    def get_order(self, user, related=False):
        """Возвращает экземпляр незавершенного Заказа текущего пользователя"""
        return Orders.objects.incomplete_order(user=user, related=related)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_steps = list()
        for i, step in enumerate(steps_links, start=1):
            step_url, step_view = step
            order_steps.append({
                'name': step_view.step_name,
                'url': step_url if i < self.step else None,
                'is_current': i == self.step
            })
        context.update({
            'step_name': self.step_name,
            'order_steps': order_steps,
        })
        return context


class OrderCreateStep1View(OrderMixin, PageInfoMixin, generic.FormView):
    """Первый этап оформления Заказа (Персональные данные)"""

    success_url = reverse_lazy('order_create_step_2')
    page_title = _('Order: personal data')
    step_name = _('Personal data')

    def get_initial(self):
        obj = self.request.user
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial.update({
                'phone_number': obj.profile.phone_number,
                'patronymic': obj.profile.patronymic,
            })
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs.update({
                'instance': self.request.user,
            })
        return kwargs

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return OrderStep1AuthorizedForm
        return OrderStep1NotAuthorizedForm

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            registration(request=self.request, registration_form=form)
        if form.changed_data:
            user_fields = ['first_name', 'last_name', 'email']
            profile_fields = ['patronymic', 'phone']

            update_instance_from_form(form=form, instance=form.instance, fields=user_fields)
            update_instance_from_form(form=form, instance=form.instance.profile, fields=profile_fields)

        if not Orders.objects.incomplete_order(user=self.request.user):
            Orders.objects.create(user=self.request.user)
        return super().form_valid(form)


class OrderCreateStep2View(OrderMixin, PageInfoMixin, LoginRequiredMixin, generic.FormView):
    """Второй этап оформления Заказа (Способ доставки)"""

    success_url = reverse_lazy('order_create_step_3')
    form_class = OrderStep2Form
    page_title = _('Order: delivery')
    step_name = _('Delivery method')
    step = 2

    def get_initial(self):
        initial = super().get_initial()
        order = self.get_order(user=self.request.user)
        if order:
            initial.update({
                'delivery': order.delivery,
                'city': order.city,
                'address': order.address,
            })
        return initial

    def form_valid(self, form):
        order = self.get_order(user=self.request.user)
        order.delivery = form.cleaned_data.get('delivery')
        order.city = form.cleaned_data.get('city')
        order.address = form.cleaned_data.get('address')
        order.save(update_fields=['delivery', 'city', 'address'])
        return super().form_valid(form)


class OrderCreateStep3View(OrderMixin, PageInfoMixin, LoginRequiredMixin, generic.FormView):
    """Третий этап оформления Заказа (Способ оплаты)"""

    success_url = reverse_lazy('order_create_confirmation')
    form_class = OrderStep3Form
    page_title = _('Order: payment')
    step_name = _('Payment method')
    step = 3

    def form_valid(self, form):
        order = self.get_order(user=self.request.user)
        order.payment = form.cleaned_data.get('payment')
        order.save(update_fields=['payment'])
        return super().form_valid(form)


class OrderConfirmationView(OrderMixin, PageInfoMixin, LoginRequiredMixin, generic.FormView):
    """Четвертый этап оформления Заказа (Проверка
    и подтверждение данных)"""

    # success_url = reverse_lazy('order_create_confirmation')
    form_class = OrderConfirmationForm
    page_title = _('Order: confirmation')
    step_name = _('Completion')
    step = 4

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        order = self.get_order(user=self.request.user, related=True)
        data.update({
            'order_data': {
                'Date, time': order.date_time.strftime('%d %B %Y, %H:%M'),
                'Receiver': f'{order.user.last_name} {order.user.first_name} {order.user.profile.patronymic}',
                'Phone': order.user.profile.phone_number_formatted,
                'Total sum': order.total_sum,
                'City': order.city,
                'Address': order.address,
                'Delivery method': order.delivery.name,
                'Payment method': order.payment.name,
            }
        })
        return data


steps_links = (
    (reverse_lazy('order_create'), OrderCreateStep1View, ),
    (reverse_lazy('order_create_step_2'), OrderCreateStep2View, ),
    (reverse_lazy('order_create_step_3'), OrderCreateStep3View, ),
    (reverse_lazy('order_create_confirmation'), OrderConfirmationView, ),
)
