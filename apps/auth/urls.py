from django.urls import path

from .views.login import LoginViaEmailView
from .views.logout import LogoutView
from .views.oauth import OAuthGoogleView
from .views.refresh import RefreshView
from .views.register import RegisterEmailView

urlpatterns = [
    path("auth/login/email/", LoginViaEmailView.as_view(), name="login-email"),
    path("auth/login/google/", OAuthGoogleView.as_view(), name="login-google"),
    path("auth/register/email/", RegisterEmailView.as_view(), name="register"),
    path("auth/refresh/", RefreshView.as_view(), name="refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]
