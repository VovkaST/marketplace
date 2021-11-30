from app_sellers.views import GoodDetailView, SellerDetailView
from django.urls import path

urlpatterns = [
    path("<slug>/", SellerDetailView.as_view(), name="seller_detail"),
    path("catalog/product/<int:pk>/", GoodDetailView.as_view(), name="prod_detail"),
]
