from services.cache import basket_cache_save


class SessionDataCollector:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.create()
        basket_cache_save(session_id=request.session.session_key, user_id=request.user.id)
        return self.get_response(request)
