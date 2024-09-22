from django.urls import path
from . import views
from blog.views import gallery
from django.conf import settings
from django.conf.urls.static import static
from .forms import NewsForm



urlpatterns = [
    path('', views.news_content, name="main"),
    path('gallery/', views.gallery, name="gallery"),
    path('add_news/', views.add_news, name="add_news"),
    
]


    # Url и функция, которая вернет картинку

 # включаем возможность обработки картинок
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)