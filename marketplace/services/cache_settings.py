SESSION_USER_DATA_CACHE_PREFIX = 'session_user_data'
GOODS_IN_BASKET_CACHE_PREFIX = f'{SESSION_USER_DATA_CACHE_PREFIX}_goods_in_basket'
BASKET_TOTAL_SUM_CACHE_PREFIX = f'{SESSION_USER_DATA_CACHE_PREFIX}_basket_total_sum'

cache_settings = {
    # Длительность кэша страницы информации о продавце
    'seller_info_life_time': 60 * 60 * 24,

    # длительность кэша для баннеров на главной странице
    'main_banners_cache': 600,
   
    # длительность кэша для баннеров на главной странице
    'categories_cache_value': 600,

    # длительность кэша пользовательской корзины
    'basket_life_time': 60 * 60 * 24,
}

