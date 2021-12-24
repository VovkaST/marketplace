from app_sellers.views import AddReviews, GoodDetailView, SellerDetailView, SellersListView
from django.urls import path

urlpatterns = [
    path("all/", SellersListView.as_view(), name="sellers_list"),
    path("catalog/product/<int:pk>/", GoodDetailView.as_view(), name="prod_detail"),
    path("add-review/<int:pk>/", AddReviews.as_view(), name="add_review"),
    path("<slug>/", SellerDetailView.as_view(), name="seller_detail"),
]
