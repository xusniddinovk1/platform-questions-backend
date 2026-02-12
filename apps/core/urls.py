from django.urls import path
from apps.core.views import HealthCheckView
from apps.questions.views.answer import AnswerCreateAPIView
from apps.questions.views.question import QuestionListAPIView, QuestionDetailAPIView

urlpatterns = [
    path("health", HealthCheckView.as_view(),
         name="health"),
    path("questions/", QuestionListAPIView.as_view(), name="question-list"),
    path("questions/<int:pk>/", QuestionDetailAPIView.as_view(), name="question-detail"),

    # path("questions/<int:question_id>/answers/",
    # AnswerListByQuestionAPIView.as_view(), name="answer-list"),
    path("answers/", AnswerCreateAPIView.as_view(), name="answer-create"),
]
