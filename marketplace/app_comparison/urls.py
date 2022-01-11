from django.urls import path

from app_comparison.views import (
    ComparisonAddView,
    ComparisonRemoveView,
    ComparisonView,
)


urlpatterns = [
    path('', ComparisonView.as_view(), name='comparison'),
    path('add/', ComparisonAddView.as_view(), name='comparison_add'),
    path('remove/', ComparisonRemoveView.as_view(), name='comparison_remove'),
]
