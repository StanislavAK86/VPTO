from django.urls import path
#from . import views

from django.conf import settings
from django.conf.urls.static import static
from .forms import NewsForm, AuthorizationForm
from .views import NewsContentView, GalleryView, AddNewsView, AboutView, AuthorizationView



urlpatterns = [
    path('', NewsContentView.as_view(), name="Главная"),
    path('gallery/', GalleryView.as_view(), name="Галерея"),
    path('add_news/', AddNewsView.as_view(), name="add_news"),
    path('about/', AboutView.as_view(), name="О нас"),
    path('authorization/', AuthorizationView.as_view(), name="authorization"),
    #path('nav/', views.nav, name="nav_menu"),
    
]


    # Url и функция, которая вернет картинку

 # включаем возможность обработки картинок
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)