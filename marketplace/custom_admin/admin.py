# fmt: off
from custom_admin.views import (  # isort:skip
    ClearAllCacheView,  # isort:skip
    GenerateBalancesView,  # isort:skip
    GenerateGoodsView,  # isort:skip
    GenerateSellersView,  # isort:skip
    ObjectGenerationView,  # isort:skip
    SettingsView, GenerateOrdersView,  # isort:skip
)  # isort:skip
# fmt: on

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
            ),
            path(
                "object-generation/",
                include(
                    [
                        path(
                            "", ObjectGenerationView.as_view(), name="object_generation"
                        ),
                        path(
                            "generate-balances/",
                            GenerateBalancesView.as_view(),
                            name="generate_balances",
                        ),
                        path(
                            "generate-goods/",
                            GenerateGoodsView.as_view(),
                            name="generate_goods",
                        ),
                        path(
                            "generate-sellers/",
                            GenerateSellersView.as_view(),
                            name="generate_sellers",
                        ),
                        path(
                            "generate-orders/",
                            GenerateOrdersView.as_view(),
                            name="generate_orders",
                        ),
                    ]
                ),
            ),
        ] + urlpatterns
        return urlpatterns
