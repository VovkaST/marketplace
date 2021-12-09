from django.contrib.auth.mixins import (
    AccessMixin,
    LoginRequiredMixin,
)
from django.core.exceptions import BadRequest
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic.base import ContextMixin

from app_basket.models import Basket
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
from services.basket import (
    complete_order,
    get_order_summary,
)
from services.utils import update_instance_from_form


class OrderBaseMixin:
    prefetch_related_objects = False

    def get_order(self, user) -> Orders:
        """Возвращает экземпляр незавершенного Заказа текущего
        пользователя (атрибут self.order). В случае отсутствия
        вычисляет его."""
        if not getattr(self, 'order', None):
            self.order = Orders.objects.incomplete_order(user=user, related=self.prefetch_related_objects)
        return self.order


class OrderRequiredMixin(OrderBaseMixin, AccessMixin):
    """Миксин обязательности наличия инициализированного Заказа"""

    def dispatch(self, request, *args, **kwargs):
        self.get_order(user=self.request.user)
        if not self.order:
            raise BadRequest(_('Order is not initialized'))
        return super().dispatch(request, *args, **kwargs)


class BasketRequiredMixin(AccessMixin):
    """Миксин обязательности наличия товаров в Корзине"""
    def dispatch(self, request, *args, **kwargs):
        if not Basket.objects.user_basket(session_id=request.session.session_key):
            raise BadRequest(_('Basket is empty'))
        return super().dispatch(request, *args, **kwargs)


class OrderMixin(OrderBaseMixin, ContextMixin):
    """Миксин работы с Заказами и добавления данных по его этапам."""

    template_name = 'app_orders/order_create.html'
    form_template_name = 'app_orders/order_form.html'
    step_name = None
    step = 1
    step_fields = list()

    def get_initial(self):
        """Получает данные полей незавершенного Заказа пользователя
        в соответствии с указанными в self.step_fields и использует
        их в качестве инициализирующих форму."""
        initial = super().get_initial()
        order = self.get_order(user=self.request.user)
        if order:
            for field in self.step_fields:
                initial.update({field: getattr(order, field)})
        return initial

    def form_valid(self, form):
        """Получает экземпляр оформляемого Заказа, заполняет
        (обновляет) поля, указанные в self.step_fields,
        и сохраняет объект в БД."""
        order = self.get_order(user=self.request.user)
        if order and self.step_fields:
            for field in self.step_fields:
                setattr(order, field, form.cleaned_data.get(field))
            order.save(update_fields=self.step_fields)
        return super().form_valid(form)

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
            'form_template': self.form_template_name
        })
        return context


class OrderCreateStep1View(OrderMixin, BasketRequiredMixin, PageInfoMixin, generic.FormView):
    """Первый этап оформления Заказа (Персональные данные)"""

    success_url = reverse_lazy('order_create_step_2')
    page_title = _('Order: personal data')
    step_name = _('Personal data')

    def get_initial(self):
        obj = self.request.user
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial.update({
                'patronymic': obj.profile.patronymic,
                'phone_number': obj.profile.phone_number,
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


class OrderCreateStep2View(OrderMixin, PageInfoMixin, LoginRequiredMixin,
                           OrderRequiredMixin, BasketRequiredMixin,
                           generic.FormView):
    """Второй этап оформления Заказа (Способ доставки)"""

    success_url = reverse_lazy('order_create_step_3')
    form_class = OrderStep2Form
    page_title = _('Order: delivery')
    step_name = _('Delivery method')
    step = 2
    step_fields = ['delivery', 'city', 'address']


class OrderCreateStep3View(OrderMixin, PageInfoMixin, LoginRequiredMixin,
                           OrderRequiredMixin, BasketRequiredMixin,
                           generic.FormView):
    """Третий этап оформления Заказа (Способ оплаты)"""

    form_template_name = 'app_orders/payment_step.html'
    success_url = reverse_lazy('order_create_confirmation')
    form_class = OrderStep3Form
    page_title = _('Order: payment')
    step_name = _('Payment method')
    step = 3
    step_fields = ['payment', 'bank_account']


class OrderConfirmationView(OrderMixin, PageInfoMixin, LoginRequiredMixin,
                            OrderRequiredMixin, BasketRequiredMixin,
                            generic.FormView):
    """Четвертый этап оформления Заказа (Проверка
    и подтверждение данных)"""

    success_url = reverse_lazy('basket')
    form_class = OrderConfirmationForm
    page_title = _('Order: confirmation')
    step_name = _('Completion')
    step = 4
    step_fields = ['comment']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        summary = get_order_summary(user=self.request.user)
        summary.update({
            _('Total sum'): self.request.basket_total_sum,
        })
        data.update({
            'order_data': summary,
        })
        return data

    def form_valid(self, form):
        self.order.comment = form.cleaned_data['comment']
        complete_order(user=self.request.user, order=self.order)
        self.order.save(force_update=True, update_fields=['comment', 'total_sum', 'confirmed'])
        return HttpResponseRedirect(self.get_success_url())


steps_links = (
    (reverse_lazy('order_create'), OrderCreateStep1View, ),
    (reverse_lazy('order_create_step_2'), OrderCreateStep2View, ),
    (reverse_lazy('order_create_step_3'), OrderCreateStep3View, ),
    (reverse_lazy('order_create_confirmation'), OrderConfirmationView, ),
)
