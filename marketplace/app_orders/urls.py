from django.urls import path

from app_orders.views import OrderCreateView


urlpatterns = [
    path('new/', OrderCreateView.as_view(), name='order_create'),
]
