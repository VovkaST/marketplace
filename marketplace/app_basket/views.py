from django.db.models import F
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import ContextMixin

from app_basket.forms import PurchasePerformForm
from app_basket.models import Basket
from services.basket import (
    add_item_to_basket,
    delete_item_from_basket,
    get_goods_quantity_in_basket,
    patch_item_in_basket,
    perform_purchase,
)
from services.utils import get_username_or_session_key


class BasketViewMixin(ContextMixin):
    template_name = 'app_shops/basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goods = Basket.objects.user_basket(self.request).select_related('reservation__good').annotate(
            sum=F('reservation__price') * F('quantity')
        )
        context.update({
            'goods': goods,
            'total_sum': sum([item.balance.price * item.quantity for item in goods]),
            'cache_key': get_username_or_session_key(self.request),
        })
        return context


class BasketHandlingBaseView(generic.FormView):
    form_class = PurchasePerformForm
    success_url = reverse_lazy('index')


class BasketView(BasketViewMixin, BasketHandlingBaseView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid(request=self.request):
            return self.form_invalid(form)
        return self.form_valid(form=form)

    def form_valid(self, form):
        sale = perform_purchase(request=self.request)
        return super().form_valid(form=form)


class BasketPatchItemView(BasketViewMixin, BasketHandlingBaseView):
    def post(self, request, *args, **kwargs):
        error = patch_item_in_basket(request=request)
        return JsonResponse({
            'success': not error,
            'error': error,
            'basket_fullness': get_goods_quantity_in_basket(request=request),
        })


class BasketDeleteItemView(BasketViewMixin, BasketHandlingBaseView):
    def post(self, request, *args, **kwargs):
        error = delete_item_from_basket(request=request)
        return JsonResponse({
            'success': not error,
            'error': error,
            'basket_fullness': get_goods_quantity_in_basket(request=request),
        })


class BasketAddItemView(BasketViewMixin, BasketHandlingBaseView):
    def post(self, request, *args, **kwargs):
        error = add_item_to_basket(request=request)
        return JsonResponse({
            'success': not error,
            'error': error,
            'basket_fullness': get_goods_quantity_in_basket(request=request),
        })
