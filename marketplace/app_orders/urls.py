from django.urls import path

from app_orders.views import (
    OrderConfirmationView,
    OrderCreateStep1View,
    OrderCreateStep2View,
    OrderCreateStep3View,
)

urlpatterns = [
    path('new/', OrderCreateStep1View.as_view(), name='order_create'),
    path('new/?step=2', OrderCreateStep2View.as_view(), name='order_create_step_2'),
    path('new/?step=3', OrderCreateStep3View.as_view(), name='order_create_step_3'),
    path('new/?step=confirmation', OrderConfirmationView.as_view(), name='order_create_confirmation'),
]
