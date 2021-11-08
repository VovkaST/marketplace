from django.urls import reverse_lazy
from django.views import generic

from app_orders.forms import (
    OrderConfirmationForm,
    OrderStep1AuthorizedForm,
    OrderStep1NotAuthorizedForm,
    OrderStep2Form,
    OrderStep3Form,
)
from main.views import PageInfoMixin


class OrderMixin(PageInfoMixin):
    template_name = 'app_orders/order_create.html'


class OrderCreateStep1View(OrderMixin, generic.FormView):
    success_url = reverse_lazy('order_create_step_2')
    page_title = 'Заказ: личные данные'

    def get_initial(self):
        obj = self.request.user
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial.update({
                'phone': obj.profile.phone_number,
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


class OrderCreateStep2View(OrderMixin, generic.FormView):
    success_url = reverse_lazy('order_create_step_3')
    form_class = OrderStep2Form
    page_title = 'Заказ: доставка'


class OrderCreateStep3View(OrderMixin, generic.FormView):
    success_url = reverse_lazy('order_create_confirmation')
    form_class = OrderStep3Form
    page_title = 'Заказ: оплата'


class OrderConfirmationView(OrderMixin, generic.FormView):
    # success_url = reverse_lazy('order_create_confirmation')
    form_class = OrderConfirmationForm
    page_title = 'Заказ: подтверждение'
