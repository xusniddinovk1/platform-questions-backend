from django.urls import path, include
from apps.core.views import HealthCheckView

urlpatterns = [
    path("", include("apps.questions.urls")),
    path("health/", HealthCheckView.as_view(), name="health"),
]
