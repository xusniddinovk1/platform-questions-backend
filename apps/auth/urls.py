from django.urls import path

from .views.confirm_email import EmailConfirmAPIView
from .views.login import LoginViaEmailView
from .views.logout import LogoutView
from .views.me import MeView
from .views.oauth import GoogleAuthURLView, GoogleCallbackView
from .views.refresh import RefreshView
from .views.register import RegisterEmailView

urlpatterns = [
    path("auth/login/email/", LoginViaEmailView.as_view(), name="login-email"),
    path("auth/register/email/", RegisterEmailView.as_view(), name="register"),
    path("auth/refresh/", RefreshView.as_view(), name="refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", MeView.as_view(), name="me-user"),
    path(
        "auth/confirm/<uidb64>/<token>/",
        EmailConfirmAPIView.as_view(),
        name="confirm_email",
    ),
    # Google OAuth 2.0 (OpenID Connect)
    path("auth/google/url/", GoogleAuthURLView.as_view(), name="google-auth-url"),
    path(
        "auth/google/callback/",
        GoogleCallbackView.as_view(),
        name="google-callback",
    ),
]
