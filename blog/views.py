from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import request
from django.views.decorators.cache import cache_page
from .models import News
# from .models import media_file
from .models import ImageGroup, Image

info = {
    "name":"Петр",
    "id": [
        {1:"Андрей"},
        {2:"Михаил"}
    ],
    "menu": [
        {"title": "Привет"},
        {"title": "Мир"}
        ]
}

news_cont = {
    "news" : [
    {"autor" : "admin",
    "date" : "21/02/2024",
    "text" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo, dignissimos nihil accusamus velit mollitia ad a natus aperiam repellat, fugiat itaque quaerat ea commodi voluptate. Ullam eos delectus cumque doloremque."},

    {"autor" : "Андрей",
    "date" : "24/02/2024",
    "text" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo, dignissimos nihil accusamus velit mollitia ad a natus aperiam repellat, fugiat itaque quaerat ea commodi voluptate. Ullam eos delectus cumque doloremque."},
    
    {"autor" : "Петр",
    "date" : "27/02/2024",
    "text" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo, dignissimos nihil accusamus velit mollitia ad a natus aperiam repellat, fugiat itaque quaerat ea commodi voluptate. Ullam eos delectus cumque doloremque."}]
}


# Create your views here.


def news_content(requerst):
        # считаем параметры из GET-запроса
    sort = requerst.GET.get('sort', 'date')
    order = requerst.GET.get('order', 'asc')

    # Проверяем дали ли мы разрешение на сортировку по этому полю
    valid_sort_fields = {'date', 'views', 'adds'}
    if sort not in valid_sort_fields:
        sort = 'date'

    # Обрабатываем направление сортировки
    if order == 'desc':
        order_by = sort
    else:
        order_by = f'-{sort}'
    news = News.objects.all().order_by(order_by)
    context = {'news': news}
    return render(requerst, 'news.html', context=context)
    #return render(requerst, 'news.html', context=news_cont)

def nav(requerst):
    return render(requerst, 'nav.html')


# def gallery(requerst):
#     return render(requerst, 'blog/gallery.html')

# def home_page(request):
#     # получаем все значения модели
#     data = media_file.objects.all()
#     return render(request, 'blog/gallery.html', {'data': data})

def gallery(request):
    groups = ImageGroup.objects.all()
    context = {
        'groups': groups
    }
    return render(request, 'blog/gallery.html', context)