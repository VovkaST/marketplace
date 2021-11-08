import json

from custom_admin.forms import ClearCacheForm
from custom_admin.utlis import clear_cache
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from loguru import logger


class SettingsView(TemplateView):
    template_name = "admin/settings.html"

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        cache_form = ClearCacheForm()
        context["cache_form"] = cache_form
        return context


class ClearAllCacheView(View):
    def post(self, request, *args, **kwargs):
        # fmt: off
        try:
            for cache in settings.CACHES:
                clear_cache(cache)
                logger.info(f'Successfully cleared "{cache}" cache')  # isort:skip
            response = {'message': 'Successfully cleared all cache'}  # isort:skip
            return JsonResponse(data=json.dumps(response), status=200, safe=False)
        except Exception as err:
            logger.info(
                f'Couldn`t clear cache, something went wrong. Received error: {err}'  # isort:skip
            )
            response = {
                'message': f'Couldn`t clear cache, something went wrong. Received error: {err}'  # isort:skip
            }
            return JsonResponse(data=json.dumps(response), status=400, safe=False)
        # fmt: on
