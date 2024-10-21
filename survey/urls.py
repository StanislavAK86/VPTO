from django.urls import path
from . import views

from .views import (
    GroupSelectionView,
    StartSurveyView,
    QuestionView,
    ResultsView,
    AddQuestionView,
    AllResultsView,
)
app_name = 'survey'

urlpatterns = [
    path('group_selection/', GroupSelectionView.as_view(), name='group_selection'),
    path('start/', StartSurveyView.as_view(), name='start_survey'),
    path('question/<int:question_id>/', QuestionView.as_view(), name='question'),
    path('results/', ResultsView.as_view(), name='results'),
    path('all_results/', AllResultsView.as_view(), name='all_results'),
    path('add_question/', AddQuestionView.as_view(), name='add_question'),
]