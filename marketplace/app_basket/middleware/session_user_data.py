from services.cache import basket_cache


class SessionDataCollector:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        basket_cache(request=request)
        return self.get_response(request)
