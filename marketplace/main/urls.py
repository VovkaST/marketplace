from django.urls import path
from main import views

urlpatterns = [
    path('', views.MarketMain.as_view(), name='main'),
    path('contacts/', views.ContactsMain.as_view(), name='contacts'),
    path('about/', views.AboutUsView.as_view(), name='about'),
]
