from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from .forms import NewsForm, AuthorizationForm



urlpatterns = [
    path('', views.news_content, name="главная"),
    path('gallery/', views.gallery, name="галерея"),
    path('add_news/', views.add_news, name="add_news"),
    path('about/', views.about, name="о нас"),
    path('authorization/', views.authorization, name="войти"),
    path('nav/', views.nav, name="nav_menu"),
    
]


    # Url и функция, которая вернет картинку

 # включаем возможность обработки картинок
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)