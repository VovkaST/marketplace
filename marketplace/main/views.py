from django.shortcuts import render
from django.views.generic.base import View


class MarketMain(View):
    """Представление главной страницы магазина"""

    def get(self, request):
        return render(request, 'main/index.html')
