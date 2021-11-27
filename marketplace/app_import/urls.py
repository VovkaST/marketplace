from django.urls import path

from app_import.views import ImportView


urlpatterns = [
    path('', ImportView.as_view(), name='import_data'),
]
