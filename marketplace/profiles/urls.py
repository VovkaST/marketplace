from django.urls import path, include
from profiles.views import (
    AccountView,
    ClientLoginView,
    RegistrationView,
    UpdateProfile,
)


urlpatterns = [
    path('account/', AccountView.as_view(), name='account'),
    path('profile/', UpdateProfile.as_view(), name='profile'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', ClientLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
]
