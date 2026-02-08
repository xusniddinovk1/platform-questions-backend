from django.urls import path

from apps.core.views import HealthCheckView
from apps.questions.views.question import (
    QuestionListCreateAPI,
    QuestionRetrieveUpdateAPI,
)
from apps.questions.views.answer import (
    AnswerRetrieveAPI,
    MyAnswersAPI,
)

urlpatterns = [
    path("health", HealthCheckView.as_view(),
         name="health"),

    path("questions/", QuestionListCreateAPI.as_view(),
         name="question-list-create"),
    path("questions/<int:pk>/", QuestionRetrieveUpdateAPI.as_view(),
         name="question-detail"),

    path("answers/mine/", MyAnswersAPI.as_view(),
         name="answer-mine"),
    path("answers/<int:pk>/", AnswerRetrieveAPI.as_view(),
         name="answer-detail"),
]
