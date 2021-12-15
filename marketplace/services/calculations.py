from app_sellers.models import Balances


def get_final_price(price=None):
    pass


def get_biggest_price(good):
    biggest_price = Balances.objects.filter(good=good).order_by("-price").first().price
    return biggest_price


def get_lowest_price(good):
    lowest_price = Balances.objects.filter(good=good).order_by("price").first().price
    return lowest_price
