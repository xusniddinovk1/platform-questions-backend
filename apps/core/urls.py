from django.urls import path
from apps.core.views import HealthCheckView
from rest_framework.routers import DefaultRouter
from apps.questions.views import AnswerViewSet, QuestionViewSet

urlpatterns = [
    path("health", HealthCheckView.as_view()),
]

router = DefaultRouter()
router.register("questions", QuestionViewSet, basename="questions")
router.register("answers", AnswerViewSet, basename="answers")

urlpatterns.extend(router.urls)
