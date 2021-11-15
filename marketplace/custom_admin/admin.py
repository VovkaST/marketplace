from custom_admin.views import ClearAllCacheView, SettingsView
from django.apps import apps
from django.contrib import admin
from django.urls import include
from loguru import logger


class MyAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        context = {}
        app_list = self.get_app_list(request)

        logger.info(app_list)
        if extra_context:
            context.update(extra_context)
        return super().index(request, context)

    def get_urls(self):
        from django.urls import path

        urlpatterns = super().get_urls()
        urlpatterns = [
            path(
                "custom-settings/",
                include(
                    [
                        path("", SettingsView.as_view(), name="custom_settings"),
                        path(
                            "clear-all-cache/",
                            ClearAllCacheView.as_view(),
                            name="clear_all_cache",
                        ),
                    ]
                ),
            )
        ] + urlpatterns
        return urlpatterns
