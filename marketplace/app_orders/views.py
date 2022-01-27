# fmt: off
from app_basket.models import Basket  # isort:skip
from app_orders.models import Orders, OrderItems  # isort:skip
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin  # isort:skip
from django.core.exceptions import BadRequest  # isort:skip
from django.http import HttpResponseRedirect  # isort:skip
from django.shortcuts import redirect, get_object_or_404  # isort:skip
from django.urls import reverse_lazy  # isort:skip
from django.utils.translation import gettext_lazy as _  # isort:skip
from django.views import generic  # isort:skip
from django.views.generic import FormView  # isort:skip
from django.views.generic.base import ContextMixin  # isort:skip
from main.views import PageInfoMixin, CategoryMixin  # isort:skip
from services.auth import registration  # isort:skip
from services.basket import merge_baskets  # isort:skip
from services.orders import get_order_summary, complete_order
from services.cache import basket_cache_clear, order_cache_clear  # isort:skip
from services.financial import order_payment  # isort:skip
from services.orders import is_enough_goods_on_balance, write_off_balances

from services.utils import update_instance_from_form  # isort:skip

from app_orders.forms import (  # isort:skip
    OrderConfirmationForm,  # isort:skip
    OrderPaymentForm,  # isort:skip
    OrderStep1AuthorizedForm,  # isort:skip
    OrderStep1NotAuthorizedForm,  # isort:skip
    OrderStep2Form,  # isort:skip
    OrderStep3Form,  # isort:skip
)  # isort:skip
# fmt: on


class OrderBaseMixin:
    prefetch_related_objects = False

    def get_order(self, user) -> Orders:
        """Возвращает экземпляр незавершенного Заказа текущего
        пользователя (атрибут self.order). В случае отсутствия
        вычисляет его."""
        if not getattr(self, "order", None):
            self.order = Orders.objects.not_confirmed_order(
                user=user, related=self.prefetch_related_objects
            )
        return self.order


class OrderRequiredMixin(OrderBaseMixin, AccessMixin):
    """Миксин обязательности наличия инициализированного Заказа"""

    def dispatch(self, request, *args, **kwargs):
        self.get_order(user=self.request.user)
        if not self.order:
            raise BadRequest(_("Order is not initialized"))
        return super().dispatch(request, *args, **kwargs)


class BasketRequiredMixin(AccessMixin):
    """Миксин обязательности наличия товаров в Корзине"""

    def dispatch(self, request, *args, **kwargs):
        if not Basket.objects.user_basket(session_id=request.session.session_key):
            raise BadRequest(_("Basket is empty"))
        return super().dispatch(request, *args, **kwargs)


class OrderMixin(CategoryMixin, OrderBaseMixin, ContextMixin):
    """Миксин работы с Заказами и добавления данных по его этапам."""

    template_name = "app_orders/order_create.html"
    form_template_name = "app_orders/order_form.html"
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
            order_steps.append(
                {
                    "name": step_view.step_name,
                    "url": step_url if i < self.step else None,
                    "is_current": i == self.step,
                }
            )
        context.update(
            {
                "step_name": self.step_name,
                "order_steps": order_steps,
                "form_template": self.form_template_name,
            }
        )
        return context


class OrderCreateStep1View(
    OrderMixin, BasketRequiredMixin, PageInfoMixin, generic.FormView
):
    """Первый этап оформления Заказа (Персональные данные)"""

    form_template_name = "app_orders/personal_data_step.html"
    success_url = reverse_lazy("order_create_step_2")
    page_title = _("Order: personal data")
    step_name = _("Step 1. Personal data")

    def get_initial(self):
        obj = self.request.user
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial.update(
                {
                    "patronymic": obj.profile.patronymic,
                    "phone_number": obj.profile.phone_number,
                }
            )
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs.update(
                {
                    "instance": self.request.user,
                }
            )
        return kwargs

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return OrderStep1AuthorizedForm
        return OrderStep1NotAuthorizedForm

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            old_session_key = self.request.session.session_key
            registration(request=self.request, registration_form=form)
            new_session_key = self.request.session.session_key
            merge_baskets(
                old_session=old_session_key,
                new_session=new_session_key,
                user=self.request.user,
            )
        if form.changed_data:
            user_fields = ["first_name", "last_name", "email"]
            profile_fields = ["patronymic", "phone"]

            update_instance_from_form(
                form=form, instance=form.instance, fields=user_fields
            )
            update_instance_from_form(
                form=form, instance=form.instance.profile, fields=profile_fields
            )

        if not Orders.objects.not_confirmed_order(user=self.request.user):
            Orders.objects.create(user=self.request.user)
        return super().form_valid(form)


class OrderCreateStep2View(
    OrderMixin,
    PageInfoMixin,
    LoginRequiredMixin,
    OrderRequiredMixin,
    BasketRequiredMixin,
    generic.FormView,
):
    """Второй этап оформления Заказа (Способ доставки)"""

    success_url = reverse_lazy("order_create_step_3")
    form_class = OrderStep2Form
    form_template_name = "app_orders/delivery_step.html"
    page_title = _("Order: delivery")
    step_name = _("Step 2. Delivery method")
    step = 2
    step_fields = ["delivery", "city", "address"]


class OrderCreateStep3View(
    OrderMixin,
    PageInfoMixin,
    LoginRequiredMixin,
    OrderRequiredMixin,
    BasketRequiredMixin,
    generic.FormView,
):
    """Третий этап оформления Заказа (Способ оплаты)"""

    form_template_name = "app_orders/payment_step.html"
    success_url = reverse_lazy("order_create_confirmation")
    form_class = OrderStep3Form
    page_title = _("Order: payment")
    step_name = _("Step 3. Payment method")
    step = 3
    step_fields = ["payment", "bank_account"]


class OrderConfirmationView(
    OrderMixin,
    PageInfoMixin,
    LoginRequiredMixin,
    OrderRequiredMixin,
    BasketRequiredMixin,
    generic.FormView,
):
    """Четвертый этап оформления Заказа (Проверка
    и подтверждение данных)"""

    form_class = OrderConfirmationForm
    form_template_name = "app_orders/confirmation_step.html"
    page_title = _("Order: confirmation")
    step_name = _("Step 4. Completion")
    step = 4
    step_fields = ["comment"]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        order = self.get_order(user=self.request.user)
        summary = get_order_summary(order)
        session = self.request.session.session_key
        user = self.request.user if self.request.user.is_authenticated else None
        summary.update(
            {
                "total_sum": self.request.basket_total_sum,
                "items": Basket.objects.user_basket(
                    session_id=session, user_id=user.id if user else None
                ),
            }
        )
        data.update(
            {
                "order_data": summary,
            }
        )
        return data

    def get_success_url(self):
        order = self.get_order(user=self.request.user)
        return reverse_lazy("order_payment", kwargs={"pk": order.id})

    def form_valid(self, form):
        self.order.comment = form.cleaned_data["comment"]
        complete_order(session=self.request.session.session_key, user=self.request.user, order=self.order)
        self.order.save(
            force_update=True, update_fields=["comment", "total_sum", "confirmed"]
        )
        session_id = self.request.session.session_key
        basket_cache_clear(session_id=session_id)
        order_cache_clear(session_id=session_id)
        return HttpResponseRedirect(self.get_success_url())


steps_links = (
    (
        reverse_lazy("order_create"),
        OrderCreateStep1View,
    ),
    (
        reverse_lazy("order_create_step_2"),
        OrderCreateStep2View,
    ),
    (
        reverse_lazy("order_create_step_3"),
        OrderCreateStep3View,
    ),
    (
        reverse_lazy("order_create_confirmation"),
        OrderConfirmationView,
    ),
)


class OrderPaymentView(AccessMixin, CategoryMixin, PageInfoMixin, FormView):
    """
    View для отдельной оплаты заказа, если этот шаг был пропущен при
    создании заказа.
    """

    page_title = _("Order payment")
    form_class = OrderPaymentForm
    template_name = "app_orders/order_pay.html"
    success_url = reverse_lazy("ordershistory")

    def dispatch(self, request, *args, **kwargs):
        order = get_object_or_404(Orders, pk=kwargs.get("pk"))
        if order.payment_state:
            raise BadRequest(_("Order is already payed."))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "order": Orders.objects.get(id=self.kwargs.get("pk")),
            }
        )
        return context

    def form_valid(self, form):
        balance_response = is_enough_goods_on_balance(order_pk=self.kwargs.get("pk"))
        if balance_response["status"]:
            payment_response = order_payment(
                order_pk=self.kwargs.get("pk"),
                card_number=form.cleaned_data["bank_account"],
            )
            if payment_response["status"]:
                write_off_balances(order_pk=self.kwargs.get("pk"))
                return redirect(self.get_success_url())
            else:
                form.add_error("bank_account", payment_response["message"])
        else:
            form.add_error("bank_account", balance_response["message"])
        return self.form_invalid(form)


class OrderDetailView(CategoryMixin, PageInfoMixin, generic.DetailView):
    """Представление детальной страницы заказа"""

    model = Orders
    context_object_name = "order"

    @property
    def page_title(self):
        return "{} № {} details".format(_("Order"), self.get_object().id)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("delivery", "payment", "user__profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = OrderItems.objects.filter(order_id=self.object).select_related(
            "seller", "good__category"
        )
        context.update(
            {
                "order_items": items,
            }
        )
        return context
