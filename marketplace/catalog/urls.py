from catalog.views import CatalogView, CategoryDetailView
from django.urls import path

urlpatterns = [
    path("", CatalogView.as_view(), name="catalog"),
    path("<int:pk>/", CategoryDetailView.as_view(), name="category_catalog"),
]
