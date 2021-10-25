from django.urls import path
from .views import AccountView, UpdateProfile, LogoutViews, LoginViews, RegistrationView

urlpatterns = [
    path('account/', AccountView.as_view(), name='account'),
    path('profile/', UpdateProfile.as_view(), name='profile'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginViews.as_view(), name='login'),
    path('logout/', LogoutViews.as_view(), name='logout')
]
