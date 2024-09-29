from django.urls import path
#from . import views

from django.conf import settings
from django.conf.urls.static import static
from .forms import NewsForm, AuthorizationForm
from .views import NewsContent, Gallery, AddNews, About, Authorization



urlpatterns = [
    path('', NewsContent.as_view(), name="Главная"),
    path('gallery/', Gallery.as_view(), name="Галерея"),
    path('add_news/', AddNews.as_view(), name="add_news"),
    path('about/', About.as_view(), name="О нас"),
    path('authorization/', Authorization.as_view(), name="authorization"),
    #path('nav/', views.nav, name="nav_menu"),
    
]


    # Url и функция, которая вернет картинку

 # включаем возможность обработки картинок
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)