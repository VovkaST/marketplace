from django.urls import path

from app_basket.views import (
    BasketAddItemView,
    BasketDeleteItemView,
    BasketPatchItemView,
    BasketView,
)


urlpatterns = [
    path('', BasketView.as_view(), name='basket'),
    path('add/', BasketAddItemView.as_view(), name='basket_add_item'),
    path('patch/', BasketPatchItemView.as_view(), name='basket_patch_item'),
    path('delete/', BasketDeleteItemView.as_view(), name='basket_delete_item'),
]
