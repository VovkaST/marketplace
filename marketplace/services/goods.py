from django.views.generic.base import ContextMixin

from app_sellers.models import Balances


class GoodsMinPriceMixin(ContextMixin):
    """Миксин добавляет в контекст словарь goods
    с данными о минимальной цене товара."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key = self.context_object_name or 'object_list'
        goods_ids = [good['id'] for good in context[key].all().values('id')]
        placeholder = ['%s' for _ in range(len(goods_ids))]
        balances = Balances.objects.raw(f'''
            SELECT mpb.id, mpb.good_id, min(mpb.price) "min_price", mpb.quantity
              FROM mp_balances mpb
             WHERE mpb.good_id in ({','.join(placeholder)})
             GROUP BY mpb.good_id
        ''', params=goods_ids)
        goods = {
            good['id']: good
            for good in context[key]
        }
        for balance in balances:
            goods[balance.good_id].update({
                'balance_id': balance.id,
                'price': balance.price,
                'quantity': balance.quantity,
            })
        context.update({'goods': goods})
        return context
