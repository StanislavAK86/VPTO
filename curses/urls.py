from django.urls import path
from . import views
from .views import QuestionnaireView, CursesView, VideoView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(' ', CursesView.as_view(), name="Курсы"),
    path('questionnaire/', QuestionnaireView.as_view(), name="question"),
    path('cards/<int:category_id>/', VideoView.as_view(), name='card_list'),
]
