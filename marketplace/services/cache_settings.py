MINUTE = 60
DAY = 60 * 60 * 24
WEEK = 60 * 60 * 24 * 7
WEEK_x4 = WEEK * 4
MINUTES_x10 = MINUTE * 10

cache_settings = {
    # Длительность кэша страницы информации о продавце
    'seller_info_life_time': DAY,

    # длительность кэша для баннеров на главной странице
    'main_banners_cache': MINUTES_x10,
   
    # длительность кэша для баннеров на главной странице
    'categories_cache_value': MINUTES_x10,

    # длительность кэша пользовательской корзины
    'basket_life_time': DAY,

    # длительность кэша страницы контактов
    'contacts_life_time': WEEK,

    # длительность кэша страницы списка продавцов
    'sellers_list_life_time': DAY,

    # длительность кэша страницы "О нас"
    'about_life_time': WEEK_x4,

    # длительность кэша страницы сравнения товаров
    'comparison_life_time': DAY,
}
