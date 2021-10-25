from django.urls import path
from . import views

urlpatterns = [
    path('', views.MarketMain.as_view(), name='main'),

]
