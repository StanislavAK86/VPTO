from django.urls import path
#from . import views

from django.conf import settings
from django.conf.urls.static import static
from .forms import NewsForm, AuthorizationForm
from .views import NewsContent, Gallery, AddNews, About, Authorization, ImageUpdateView, ImageCreateView, ImageDeleteView, ImageGroupCreateView



urlpatterns = [
    path('', NewsContent.as_view(), name="Главная"),
    path('gallery/', Gallery.as_view(), name="Галерея"),
    path('add_news/', AddNews.as_view(), name="add_news"),
    path('about/', About.as_view(), name="О нас"),
    path('authorization/', Authorization.as_view(), name="authorization"),
    path('image/<int:pk>/edit/', ImageUpdateView.as_view(), name='image_edit'),
    path('image/add/', ImageCreateView.as_view(), name='image_add'),
    path('image/<int:pk>/delete/', ImageDeleteView.as_view(), name='image_delete'),
    path('imagegroup_add/', ImageGroupCreateView.as_view(), name='imagegroup_add'),
    #path('nav/', views.nav, name="nav_menu"),
    
]


