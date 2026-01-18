from django.urls import path
from .views import QuestionListView, QuestionDetailVIew, AnswerCreateView

urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path('questions/<int:pk>/', QuestionDetailVIew.as_view(), name='question_detail'),
    path('answers/', AnswerCreateView.as_view(), name='answer_create'),
]
