import json

# fmt: off
from app_orders.factories import (MAX_DELIVERY_METHODS, MAX_PAYMENTS_METHODS,
                                  DeliveryMethodsFactory, OrderItemsFactory,
                                  OrdersFactory, PaymentMethodsFactory)
from app_orders.models import DeliveryMethods, PaymentMethods
from app_sellers.factories import BalancesFactory, GoodsFactory, SellersFactory
from custom_admin.utlis import clear_cache
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView
from loguru import logger

from custom_admin.forms import (  # isort:skip
    ClearCacheForm,  # isort:skip
    GenerateBalancesForm,  # isort:skip
    GenerateGoodsForm,  # isort:skip
    GenerateSellersForm,
    OrdersGenerateForm,  # isort:skip
)  # isort:skip
# fmt: on


class SettingsView(TemplateView):
    """View для страницы настроек в панели администрирования"""

    template_name = "admin/settings.html"

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        cache_form = ClearCacheForm()
        context["cache_form"] = cache_form
        return context


class ObjectGenerationView(TemplateView):
    template_name = "admin/object_generation.html"


class ClearAllCacheView(View):
    """View для полной очистки кэша"""

    def post(self, request, *args, **kwargs):
        # fmt: off
        try:
            for cache in settings.CACHES:
                clear_cache(cache)
                logger.info(f'Successfully cleared "{cache}" cache')  # isort:skip
            response = {'message': 'Successfully cleared all cache'}  # isort:skip
            return JsonResponse(data=json.dumps(response), status=200, safe=False)
        except Exception as err:
            logger.info(
                f'Couldn`t clear cache, something went wrong. Received error: {err}'  # isort:skip
            )
            response = {
                'message': f'Couldn`t clear cache, something went wrong. Received error: {err}'  # isort:skip
            }
            return JsonResponse(data=json.dumps(response), status=400, safe=False)
        # fmt: on


class GeneratorBaseView(FormView):
    objects_name = ""

    def generate_objects(self, **kwargs):
        """Метод генерации объектов"""
        pass

    def form_valid(self, form):
        error = ""
        try:
            self.generate_objects(**form.cleaned_data)
        except Exception as exc:
            error = f"{self.objects_name.capitalize()} generation error: {exc.args[0]}"
            logger.error(error)
        response = {
            "success": not error,
            "message": error or f"{self.objects_name}s successfully created!",
            "redirect": self.success_url,
        }
        return JsonResponse(data=response, status=200, safe=False)


class GenerateBalancesView(GeneratorBaseView):
    """
    Служит для создания балансов товаров у продавцов. В зависимости от нужд разработчика или другого сотрудника,
    можно сгенерировать несколько балансов для одного товара (который будет у нескольких продавцов), или
    же наоборот для одного продавца (у которого будет несколько товаров)
    """

    objects_name = "Balances"
    template_name = "admin/forms/balances_generate_form.html"
    form_class = GenerateBalancesForm
    success_url = reverse_lazy("admin:app_sellers_balances_changelist")

    def generate_objects(self, single_choice, balances_quantity):
        if single_choice == "Good":
            balances = BalancesFactory.create_batch(
                size=balances_quantity, good=GoodsFactory.create()
            )
            logger.info(f"Created balances {balances}")
        elif single_choice == "Seller":
            balances = BalancesFactory.create_batch(
                size=balances_quantity,
                seller=SellersFactory.create(),
            )
            logger.info(f"Created balances {balances}")
        else:
            balances = BalancesFactory.create_batch(size=balances_quantity)
            logger.info(f"Created balances {balances}")


class GenerateGoodsView(GeneratorBaseView):
    """Генерирует заданное количество различных товаров, но без остатков у продавцов"""

    objects_name = "Goods"
    template_name = "admin/forms/goods_generate_form.html"
    form_class = GenerateGoodsForm
    success_url = reverse_lazy("admin:app_sellers_goods_changelist")

    def generate_objects(self, quantity: int):
        goods = GoodsFactory.create_batch(size=quantity)
        logger.info(f"Created goods: {goods}")


class GenerateSellersView(GeneratorBaseView):
    """Генерирует указанное количество различных продавцов, без остатков товаров"""

    objects_name = "Sellers"
    template_name = "admin/forms/sellers_generate_form.html"
    form_class = GenerateSellersForm
    success_url = reverse_lazy("admin:app_sellers_sellers_changelist")

    def generate_objects(self, quantity):
        sellers = SellersFactory.create_batch(size=quantity)
        logger.info(f"Created sellers: {sellers}")


class GenerateOrdersView(GeneratorBaseView):
    """
    Генерирует указанное количество заказов, для каждого заказа также создается по 4 вида товара,
    и для каждого товара создаются остатки у продавцов (вместе с продавцами), конечные суммы заказов
    пересчитываются в соответствии со сгенерированными ценами
    """

    objects_name = "Orders"
    template_name = "admin/forms/orders_generate_form.html"
    form_class = OrdersGenerateForm
    success_url = reverse_lazy("admin:app_orders_orderitems_changelist")

    def generate_objects(self, quantity):
        payments_methods_exists = PaymentMethods.objects.all().count()
        payments_methods_need = MAX_PAYMENTS_METHODS - payments_methods_exists
        if payments_methods_need > 0:
            PaymentMethodsFactory.create_batch(size=payments_methods_need)

        delivery_methods_exists = DeliveryMethods.objects.all().count()
        delivery_methods_need = MAX_DELIVERY_METHODS - delivery_methods_exists
        if delivery_methods_need > 0:
            DeliveryMethodsFactory.create_batch(size=delivery_methods_need)

        for i in range(quantity):
            order = OrdersFactory.create(user=self.request.user)
            order_items = OrderItemsFactory.create_batch(size=4, order=order)
            order.total_sum = 0
            for order_item in order_items:
                order.total_sum += order_item.total_price
                BalancesFactory(
                    good=order_item.good,
                    seller=order_item.seller,
                    quantity=order_item.quantity * 2,
                )
            order.total_sum += order.delivery.price
            order.save()
