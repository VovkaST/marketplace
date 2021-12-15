from django.urls import path

from app_import.views import ImportView, TaskCheckView


urlpatterns = [
    path('', ImportView.as_view(), name='import_data'),
    path('task_check/', TaskCheckView.as_view(), name='task_check'),
]
