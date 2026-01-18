from django.urls import path
from apps.questions.views import QuestionListView, QuestionDetailVIew, AnswerCreateView
from apps.core.views import HealthCheckView

urlpatterns = [
    path("health", HealthCheckView.as_view()),
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path('questions/<int:pk>/', QuestionDetailVIew.as_view(), name='question_detail'),
    path('answers/', AnswerCreateView.as_view(), name='answer_create'),
]
