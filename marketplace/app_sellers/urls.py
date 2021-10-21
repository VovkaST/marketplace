from django.urls import path

from app_sellers.views import SellerDetailView

urlpatterns = [
    path('<slug>/', SellerDetailView.as_view(), name='seller_detail'),
]
