from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import generic

from main.views import (
    CacheSettingsMixin,
    PageInfoMixin,
)
from services.basket import (
    add_item_to_basket,
    delete_item_from_basket,
    get_basket_meta,
    init_basket_formset,
    patch_item_seller,
    patch_item_quantity,
)
from services.cache import (
    basket_cache_clear,
    basket_cache_save,
)


class BasketMetaMixin:
    """Миксин обработки корзины. Получает ее мета-данные
    (кол-во товаров, общая сумма товаров в корзине), сбрасывает
    кэш и обновляет данные в нем."""

    def get_meta(self):
        user = self.request.user
        session = self.request.session.session_key
        meta = get_basket_meta(session_id=session, user_id=user.id)
        basket_cache_clear(session_id=session, username=user.username, keys=meta.values())
        basket_cache_save(session_id=session, **meta)
        return meta


class BasketView(CacheSettingsMixin, PageInfoMixin, generic.TemplateView):
    template_name = 'app_basket/basket_detail.html'
    page_title = _('Basket')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        session = self.request.session.session_key
        meta = get_basket_meta(session_id=session, user_id=user.id, items=True)
        context.update({
            'cache_key': user.username if user.is_authenticated else session,
            'items_formset': init_basket_formset(items=meta['items']),
            **meta,
        })
        return context


class BasketPatchItemQuantityView(BasketMetaMixin, generic.View):
    """Изменение количества товара в корзине."""

    def post(self, request, *args, **kwargs):
        reservation_id = request.POST.get('reservation_id')
        quantity = request.POST.get('quantity')
        obj_data, error = patch_item_quantity(
            session=request.session.session_key, reservation_id=reservation_id, quantity=quantity
        )
        return JsonResponse({
            'success': not error,
            'error': error,
            'changed_item': obj_data,
            **self.get_meta(),
        })


class BasketPatchItemSellerView(BasketMetaMixin, generic.View):
    """Выбор товара у другого продавца."""

    def post(self, request, *args, **kwargs):
        reservation_id = request.POST.get('reservation_id')
        seller_id = request.POST.get('seller')
        obj_data, error = patch_item_seller(
            session=request.session.session_key, reservation_id=reservation_id, seller=seller_id
        )
        return JsonResponse({
            'success': not error,
            'error': error,
            'changed_item': obj_data,
            **self.get_meta(),
        })


class BasketDeleteItemView(BasketMetaMixin, generic.View):
    """Удаление товара из корзины"""

    def post(self, request, *args, **kwargs):
        reservation_id = request.POST.get('reservation_id')
        error = delete_item_from_basket(session=request.session.session_key, reservation_id=reservation_id)
        return JsonResponse({
            'success': not error,
            'error': error,
            **self.get_meta(),
        })


class BasketAddItemView(BasketMetaMixin, generic.View):
    """Добавление товара в корзину."""

    def post(self, request, *args, **kwargs):
        reservation = request.POST.get('data-id')
        quantity = int(request.POST.get('quantity', 1))
        session = request.session.session_key
        user = request.user if request.user.is_authenticated else None
        obj_data, error = add_item_to_basket(user=user, session=session, reservation_id=reservation, quantity=quantity)
        return JsonResponse({
            'success': not error,
            'error': error,
            'changed_item': obj_data,
            **self.get_meta()
        })
