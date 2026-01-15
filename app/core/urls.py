from django.urls import path
from app.core.views import health_check

urlpatterns = [
    path('health', health_check),
]