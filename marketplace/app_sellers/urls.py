from app_sellers.views import AddReviews, GoodDetailView, SellerDetailView
from django.urls import path

urlpatterns = [
    path("<slug>/", SellerDetailView.as_view(), name="seller_detail"),
    path("catalog/product/<int:pk>/", GoodDetailView.as_view(), name="prod_detail"),
    path("add-review/<int:pk>/", AddReviews.as_view(), name="add_review"),
]
