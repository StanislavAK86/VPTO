from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.context_processors import request
from django.views.decorators.cache import cache_page
from .models import News
from .models import ImageGroup, Image
from .forms import NewsForm



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
    return render(requerst, 'blog/news.html', context=context)
    

def nav(requerst):
    return render(requerst, 'nav.html')


def gallery(request):
    groups = ImageGroup.objects.all()
    context = {
        'groups': groups
    }
    return render(request, 'blog/gallery.html', context)
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else: 
        form = NewsForm()

    context = {'form': form}
    return render(request, 'blog/add_news.html', context=context)