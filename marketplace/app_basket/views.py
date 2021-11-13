from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from app_basket.forms import PurchasePerformForm
from app_basket.models import Basket
from services.basket import (
    add_item_to_basket,
    delete_item_from_basket,
    get_basket_meta,
    patch_item_in_basket,
    perform_purchase,
)
from services.cache import basket_cache_save, basket_cache_clear
from services.utils import get_username_or_session_key


class BasketViewMixin(ContextMixin):
    template_name = 'app_shops/basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'cache_key': get_username_or_session_key(self.request),
            **get_basket_meta(
                session_id=self.request.session.session_key, user_id=self.request.user.id, items=True
            ),
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
        perform_purchase(request=self.request)
        return super().form_valid(form=form)


class BasketPatchItemView(BasketViewMixin, BasketHandlingBaseView):
    def post(self, request, *args, **kwargs):
        error = patch_item_in_basket(request=request)
        return JsonResponse({
            'success': not error,
            'error': error,
            **get_basket_meta(session_id=request.session.session_key, user_id=request.user.id),
        })


class BasketDeleteItemView(BasketViewMixin, BasketHandlingBaseView):
    def post(self, request, *args, **kwargs):
        error = delete_item_from_basket(request=request)
        return JsonResponse({
            'success': not error,
            'error': error,
            **get_basket_meta(session_id=request.session.session_key, user_id=request.user.id),
        })


class BasketAddItemView(BasketViewMixin, BasketHandlingBaseView):
    def post(self, request, *args, **kwargs):
        reservation = request.POST.get('data-id')
        quantity = int(request.POST.get('quantity', 1))
        session = request.session.session_key
        user = request.user if request.user.is_authenticated else None
        error = add_item_to_basket(user=user, session=session, reservation_id=reservation, quantity=quantity)
        basket_cache_clear(username=user.username, session_id=session)
        meta = basket_cache_save(user_id=user.id, session_id=session)
        return JsonResponse({
            'success': not error,
            'error': error,
            **meta
        })
