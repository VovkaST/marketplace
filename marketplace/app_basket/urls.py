from django.urls import path

from app_basket.views import (
    BasketAddItemView,
    BasketDeleteItemView,
    BasketPatchItemSellerView,
    BasketPatchItemQuantityView,
    BasketView,
)


urlpatterns = [
    path('', BasketView.as_view(), name='basket'),
    path('add/', BasketAddItemView.as_view(), name='basket_add_item'),
    path('quantity/', BasketPatchItemQuantityView.as_view(), name='basket_patch_item_quantity'),
    path('seller/', BasketPatchItemSellerView.as_view(), name='basket_patch_item_seller'),
    path('delete/', BasketDeleteItemView.as_view(), name='basket_delete_item'),
]
