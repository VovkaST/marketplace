from catalog.views import CatalogView
from django.urls import path

urlpatterns = [
    path("", CatalogView.as_view(), name="catalog"),
    path("<int:pk>", CatalogView.as_view(), name="category_catalog"),
]
