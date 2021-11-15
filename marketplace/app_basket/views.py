from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import generic

from main.views import PageInfoMixin
from services.basket import (
    add_item_to_basket,
    delete_item_from_basket,
    get_basket_meta,
    patch_item_in_basket,
)
from services.cache import basket_cache_save, basket_cache_clear


class BasketView(PageInfoMixin, generic.TemplateView):
    template_name = 'app_basket/basket_detail.html'
    page_title = _('Basket')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            **get_basket_meta(
                session_id=self.request.session.session_key, user_id=self.request.user.id, items=True
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
        error = patch_item_in_basket(request=request)
        return JsonResponse({
            'success': not error,
            'error': error,
            **get_basket_meta(session_id=request.session.session_key, user_id=request.user.id),
        })


class BasketDeleteItemView(generic.View):
    def post(self, request, *args, **kwargs):
        error = delete_item_from_basket(request=request)
        return JsonResponse({
            'success': not error,
            'error': error,
            **get_basket_meta(session_id=request.session.session_key, user_id=request.user.id),
        })


class BasketAddItemView(generic.View):
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
