from django.urls import path

from .views.login import LoginViaEmailView, LoginViaPhoneView
from .views.logout import LogoutView
from .views.oauth import OAuthGoogleView
from .views.refresh import RefreshView
from .views.register import RegisterView

urlpatterns = [
    path("login/email/", LoginViaEmailView.as_view(), name="login-email"),
    path("login/phone/", LoginViaPhoneView.as_view(), name="login-phone"),
    path("login/google/", OAuthGoogleView.as_view(), name="login-google"),
    path("register/", RegisterView.as_view(), name="register"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
