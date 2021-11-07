from django.views import generic

from app_orders.models import Orders


class OrderCreateView(generic.CreateView):
    model = Orders
    fields = '__all__'
    template_name = 'app_orders/order_create.html'
