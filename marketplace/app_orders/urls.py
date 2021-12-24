# fmt: off
from app_orders.views import (  # isort:skip
    OrderConfirmationView,  # isort:skip
    OrderCreateStep1View,  # isort:skip
    OrderCreateStep2View,  # isort:skip
    OrderCreateStep3View,  # isort:skip
    OrderDetailView,  # isort:skip
    OrderPaymentView,  # isort:skip
)  # isort:skip
from django.urls import include, path  # isort:skip
# fmt: on

urlpatterns = [
    path("new/", OrderCreateStep1View.as_view(), name="order_create"),
    path("new/?step=2", OrderCreateStep2View.as_view(), name="order_create_step_2"),
    path("new/?step=3", OrderCreateStep3View.as_view(), name="order_create_step_3"),
    path(
        "new/?step=confirmation",
        OrderConfirmationView.as_view(),
        name="order_create_confirmation",
    ),
    path("<int:pk>/payment/", OrderPaymentView.as_view(), name="order_payment"),
    path("<int:pk>/view/", OrderDetailView.as_view(), name="order_detail"),
]
