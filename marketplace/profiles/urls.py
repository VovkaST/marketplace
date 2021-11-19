from django.urls import include, path

# fmt: off
from profiles.views import (AccountView, ClientLoginView, RegistrationView,  # isort:skip
                            UpdateProfile, ViewsHistoryView, OrdersHistoryView)  # isort:skip

# fmt: on

urlpatterns = [
    path("account/", AccountView.as_view(), name="account"),
    path("profile/", UpdateProfile.as_view(), name="profile"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", ClientLoginView.as_view(), name="login"),
    path("history-view/", ViewsHistoryView.as_view(), name="historyview"),
    path("orders-history/", OrdersHistoryView.as_view(), name="ordershistory"),
    path("", include("django.contrib.auth.urls")),
]
