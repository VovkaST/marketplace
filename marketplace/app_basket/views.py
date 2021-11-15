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
    patch_item_in_basket,
)
from services.cache import basket_cache_save


class BasketView(CacheSettingsMixin, PageInfoMixin, generic.TemplateView):
    template_name = 'app_basket/basket_detail.html'
    page_title = _('Basket')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        session = self.request.session.session_key
        context.update({
            'cache_key': user.username if user.is_authenticated else session,
            **get_basket_meta(
                session_id=session, user_id=user.id, items=True
            ),
        })
        return context

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if not form.is_valid(request=self.request):
    #         return self.form_invalid(form)
    #     return self.form_valid(form=form)
    #
    # def form_valid(self, form):
    #     perform_purchase(request=self.request)
    #     return super().form_valid(form=form)


class BasketPatchItemView(generic.View):
    def post(self, request, *args, **kwargs):
        reservation_id = request.POST.get('basket_item_patch')
        quantity = request.POST.get('quantity')
        user = request.user
        session = request.session.session_key
        error = patch_item_in_basket(
            session=session, reservation_id=reservation_id, quantity=quantity
        )
        meta = get_basket_meta(session_id=session, user_id=user.id)
        basket_cache_save(user_id=user.id, session_id=session, **meta)
        return JsonResponse({
            'success': not error,
            'error': error,
            **meta,
        })


class BasketDeleteItemView(generic.View):
    def post(self, request, *args, **kwargs):
        user = request.user
        session = request.session.session_key
        reservation_id = request.POST.get('basket_item_delete')
        error = delete_item_from_basket(session=session, reservation_id=reservation_id)
        meta = get_basket_meta(session_id=session, user_id=user.id)
        basket_cache_save(user_id=user.id, session_id=session, **meta)
        return JsonResponse({
            'success': not error,
            'error': error,
            **meta,
        })


class BasketAddItemView(generic.View):
    def post(self, request, *args, **kwargs):
        reservation = request.POST.get('data-id')
        quantity = int(request.POST.get('quantity', 1))
        session = request.session.session_key
        user = request.user if request.user.is_authenticated else None
        error = add_item_to_basket(user=user, session=session, reservation_id=reservation, quantity=quantity)
        meta = get_basket_meta(session_id=session, user_id=self.request.user.id)
        basket_cache_save(session_id=session, **meta)
        return JsonResponse({
            'success': not error,
            'error': error,
            **meta
        })
