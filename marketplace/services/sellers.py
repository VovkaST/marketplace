from typing import Union, List, Tuple

from app_sellers.models import Goods, Sellers


def get_choices_sellers_by_good(good: Union[Goods, int]) -> List[Tuple]:
    """Возвращает список продавцов определенного товара
    для помещения в ChoiceField.

    :param good: Товар (экземпляр или id) для фильтрации продавцов.
    :return: Список продавцов в виде множества.
    """
    sellers = Sellers.objects.by_good(good=good).values('id', 'name', 'balance_owner__price')
    return [
        (seller['id'], f'{seller["name"]} ({seller["balance_owner__price"]})')
        for seller in sellers
    ]
