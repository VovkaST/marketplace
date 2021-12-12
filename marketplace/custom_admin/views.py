import json

from app_sellers.factories import BalancesFactory, GoodsFactory, SellersFactory
from custom_admin.utlis import clear_cache
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import FormView, TemplateView
from loguru import logger

# fmt: off
from custom_admin.forms import (  # isort:skip
    ClearCacheForm,  # isort:skip
    GenerateBalancesForm,  # isort:skip
    GenerateGoodsForm,  # isort:skip
    GenerateSellersForm,  # isort:skip
)  # isort:skip
# fmt: on


class SettingsView(TemplateView):
    template_name = "admin/settings.html"

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        cache_form = ClearCacheForm()
        context["cache_form"] = cache_form
        return context


class ObjectGenerationView(TemplateView):
    template_name = "admin/object_generation.html"


class ClearAllCacheView(View):
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


class GenerateBalancesView(FormView):
    """
    Служит для создания балансов товаров у продавцов. В зависимости от нужд разработчика или другого сотрудника,
    можно сгенерировать несколько балансов для одного товара (который будет у нескольких продавцов), или
    же наоборот для одного продавца (у которого будет несколько товаров)
    """

    template_name = "admin/forms/balances_generate_form.html"
    form_class = GenerateBalancesForm

    def form_valid(self, form):
        if form.cleaned_data["single_choice"] == "2":
            balances = BalancesFactory.create_batch(
                size=form.cleaned_data["balances_quantity"], good=GoodsFactory.create()
            )
            logger.info(f"Created balances {balances}")
        elif form.cleaned_data["single_choice"] == "3":
            balances = BalancesFactory.create_batch(
                size=form.cleaned_data["balances_quantity"],
                seller=SellersFactory.create(),
            )
            logger.info(f"Created balances {balances}")
        else:
            balances = BalancesFactory.create_batch(
                size=form.cleaned_data["balances_quantity"]
            )
            logger.info(f"Created balances {balances}")
        response = {"message": "Balances successfully created!"}
        return JsonResponse(data=json.dumps(response), status=200, safe=False)


class GenerateGoodsView(FormView):
    template_name = "admin/forms/goods_generate_form.html"
    form_class = GenerateGoodsForm

    def form_valid(self, form):
        goods = GoodsFactory.create_batch(size=form.cleaned_data["quantity"])
        logger.info(f"Created goods: {goods}")
        response = {"message": "Goods successfully created!"}
        return JsonResponse(data=json.dumps(response), status=200, safe=False)


class GenerateSellersView(FormView):
    template_name = "admin/forms/sellers_generate_form.html"
    form_class = GenerateSellersForm

    def form_valid(self, form):
        sellers = SellersFactory.create_batch(size=form.cleaned_data["quantity"])
        logger.info(f"Created sellers: {sellers}")
        response = {"message": "Sellers successfully created!"}
        return JsonResponse(data=json.dumps(response), status=200, safe=False)
