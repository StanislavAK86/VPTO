from django.urls import path
from . import views
from blog.views import gallery
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('', views.news_content, name="main"),
    path('gallery', views.gallery, name="gallery"),
]


    # Url и функция, которая вернет картинку

 # включаем возможность обработки картинок
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)