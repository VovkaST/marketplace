from collections import defaultdict

from django.contrib.auth.models import User
from django.db.models import F, Prefetch

from app_comparison.models import Comparison
from app_sellers.models import GoodsDescriptionsValues
from services.goods import get_cheapest_balances


def get_comparison_context(user: User, session: str) -> dict:
    user_data = {
        'user_id': user.id if user else None,
        'session': session,
    }
    description_queryset = GoodsDescriptionsValues.objects \
        .annotate(feature_value=F('feature__value'))

    comps = Comparison.objects \
        .user_comparison(**user_data) \
        .select_related('good__category') \
        .prefetch_related(Prefetch('good__description', queryset=description_queryset))

    goods_ids = [comp.good_id for comp in comps]
    balances = get_cheapest_balances(goods_ids=goods_ids)

    comp_items = defaultdict(list)
    features = defaultdict(set)
    for item in comps:
        good = item.good
        good_item = {
            'id': good.id,
            'name': good.name,
            'rating': good.rating_average,
            'features': {
                desc.feature_value: desc.value
                for desc in good.description.all()
            },
            **balances.get(good.id, dict()),
        }
        comp_items[good.category.name].append(good_item)
        features[good.category.name].update(good_item['features'].keys())
    return {
        'comp_items': dict(comp_items),
        'features': dict(features),
    }
