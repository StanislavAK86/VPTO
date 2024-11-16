from django.urls import path
from . import views
from .views import QuestionnaireView, CursesView, VideoView, VideoStreamView, VideoCreateView, VideoDeleteView

# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
    path(' ', CursesView.as_view(), name="Курсы"),
    path('questionnaire/', QuestionnaireView.as_view(), name="question"),
    path('cards/<int:category_id>/', VideoView.as_view(), name='card_list'),
    path('video/<int:video_id>/', VideoStreamView.as_view(), name='video_stream'),
    path('add/', VideoCreateView.as_view(), name='video_add'),
    path('video/<int:pk>/delete/', VideoDeleteView.as_view(), name='video_delete'),
    # path('cards/<int:pk>/delete/', VideoDeleteView.as_view(), name='video_delete'),
]
