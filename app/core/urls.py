from django.urls import path

from app.core.views import HealthCheckView

urlpatterns = [
    path("health", HealthCheckView.as_view()),
]
