from decimal import Decimal
from typing import Tuple, List

from django.contrib.auth.models import User
from django.db.models import Max, Min
from django.views.generic.base import ContextMixin

from app_comparison.models import Comparison
from app_sellers.models import Balances
from services.cache import comparison_cache_clear


class GoodsMinPriceMixin(ContextMixin):
    """Миксин добавляет в контекст словарь goods
    с данными о минимальной цене товара.
    Для корректного использования queryset должен возвращать
    данные в виде словаря (применять метод values)."""

    def get_balances(self, goods_ids, *args, **kwargs):
        return get_cheapest_balances(goods_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'goods_ids' in kwargs:
            balances = self.get_balances(**kwargs)
            goods = {
                good['id']: {**good, **balances[good['id']]}
                for good in context['object_list']
            }
            context.update({'goods': goods})
        return context


def balances_to_dict(balances):
    goods = dict()
    for balance in balances:
        goods[balance.good_id] = {
            'balance_id': balance.id,
            'price': balance.price,
            'quantity': balance.quantity,
        }
    return goods


def get_cheapest_balances(goods_ids: List[int]) -> dict:
    """Получение данных о минимальной цене товаров по их id.
    :param goods_ids: список идентификаторов товаров.
    """
    placeholder = ['%s' for _ in range(len(goods_ids))]
    balances = Balances.objects.raw(f'''
        SELECT mpb.id, mpb.good_id, min(mpb.price) "min_price", mpb.quantity
          FROM mp_balances mpb
         WHERE mpb.good_id in ({','.join(placeholder)})
         GROUP BY mpb.good_id
    ''', params=goods_ids)
    return balances_to_dict(balances)


def get_balances_in_range(goods_ids: List[int], price_min: Decimal, price_max: Decimal) -> dict:
    placeholder = ['%s' for _ in range(len(goods_ids))]
    balances = Balances.objects.raw(f'''
        SELECT mpb.id, mpb.good_id, min(mpb.price) "min_price", mpb.quantity
          FROM mp_balances mpb
         WHERE mpb.good_id in ({','.join(placeholder)})
           AND mpb.price between %s and %s
         GROUP BY mpb.good_id
    ''', params=[*goods_ids, price_min, price_max])
    return balances_to_dict(balances)


def comparison_good_add(good_id: int, user: User, session: str) -> Tuple[dict, str]:
    """Добавляет товар в пользовательский список сравнения.

    :param good_id: идентификатор товара.
    :param user: экземпляр авторизованного пользователя.
    :param session: идентификатор сессии.
    :return: Словарь с количеством товаров в списке сравнения и строка ошибки.
    """
    data, error = dict(), None
    user_data = {
        'user_id': user.id if user else None,
        'session': session,
    }
    try:
        Comparison.objects.get_or_create(good_id=good_id, **user_data)
    except Exception as exc:
        error = exc.args[0]
    data['count'] = Comparison.objects.user_comparison(**user_data).count()
    comparison_cache_clear(session=session)
    return data, error


def comparison_good_remove(good_id: int, user: User, session: str) -> Tuple[dict, str]:
    """Удаляет товар из пользовательского списка сравнения.

    :param good_id: идентификатор товара.
    :param user: экземпляр авторизованного пользователя.
    :param session: идентификатор сессии.
    :return: Словарь с количеством товаров в списке сравнения и строка ошибки.
    """
    data, error = dict(), None
    user_data = {
        'user_id': user.id if user else None,
        'session': session,
    }
    try:
        Comparison.objects.delete_good_comparison(good_id=good_id, **user_data)
    except Exception as exc:
        error = exc.args[0]
    data['count'] = Comparison.objects.user_comparison(**user_data).count()
    comparison_cache_clear(session=session)
    return data, error


def get_most_expensive_good_price():
    """Получение самой высокой в БД цены товара."""
    price = Balances.objects.aggregate(max=Max('price'))
    return price.get('max', 0)


def get_cheapest_good_price():
    """Получение самой низкой в БД цены товара."""
    price = Balances.objects.aggregate(min=Min('price'))
    return price.get('min', 0)
