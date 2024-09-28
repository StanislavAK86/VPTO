from django.shortcuts import render
from django.template.context_processors import request
from django.views.decorators.cache import cache_page
from .models import News
from .models import ImageGroup, Image
from .forms import NewsForm, AuthorizationForm
from django.views.generic import View, TemplateView, FormView

nav_menu = {
    'menu': ['Главная', 'Галерея', 'О нас', 'Курсы'],
}

class MenuMixin(View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = nav_menu['menu']
        return context

class NewsContentView(MenuMixin, TemplateView):
    template_name = 'blog/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort = self.request.GET.get('sort', 'date')
        order = self.request.GET.get('order', 'asc')

        valid_sort_fields = {'date', 'views', 'adds'}
        if sort not in valid_sort_fields:
            sort = 'date'

        if order == 'desc':
            order_by = sort
        else:
            order_by = f'-{sort}'

        news = News.objects.all().order_by(order_by)
        context['news'] = news
        return context
# def news_content(requerst):
#         # считаем параметры из GET-запроса
#     sort = requerst.GET.get('sort', 'date')
#     order = requerst.GET.get('order', 'asc')

#     # Проверяем дали ли мы разрешение на сортировку по этому полю
#     valid_sort_fields = {'date', 'views', 'adds'}
#     if sort not in valid_sort_fields:
#         sort = 'date'

#     # Обрабатываем направление сортировки
#     if order == 'desc':
#         order_by = sort
#     else:
#         order_by = f'-{sort}'
#     news = News.objects.all().order_by(order_by)
#     context = {'news': news, 'menu': nav_menu['menu']}
#     return render(requerst, 'blog/news.html', context=context)

class GalleryView(MenuMixin, TemplateView):
    template_name = 'blog/gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = ImageGroup.objects.all()
        context['menu'] = nav_menu['menu']
        return context
# def gallery(request):
#     groups = ImageGroup.objects.all()
#     context = {
#         'groups': groups, 'menu': nav_menu['menu']
#     }
#     return render(request, 'blog/gallery.html', context)


class AddNewsView(MenuMixin, FormView):
    template_name = 'blog/add_news.html'
    form_class = NewsForm
    success_url = '/'
    

    def form_valid(self, form):
        return super().form_valid(form)
    
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('/')
#     else: 
#         form = NewsForm()

#     context = {'form': form}
#     return render(request, 'blog/add_news.html', context=context)


class AboutView(MenuMixin, TemplateView):
    template_name = 'blog/about.html'
# def about(request):
#     context = {'menu': nav_menu['menu']}
#     return render(request, 'blog/about.html', context=context)


class AuthorizationView(MenuMixin, FormView):
    template_name = 'blog/authorization.html'
    form_class = AuthorizationForm
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)
# def authorization(request):
#     if request.method == 'POST':
#         form = AuthorizationForm(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('/')
#     else: 
#         form = AuthorizationForm()

#     context = {'form': form}
#     return render(request, 'blog/authorization.html', context=context)