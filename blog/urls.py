from django.urls import path
from . import views





urlpatterns = [
    path('', views.news_content, name="main"),
    path('gallery', views.gallery, name="gallery"),
]
