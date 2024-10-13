from django.shortcuts import render, redirect, reverse
from django.template.context_processors import request
from django.views.decorators.cache import cache_page
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import News
from .models import ImageGroup, Image
from .forms import NewsForm, AuthorizationForm
from django.views.generic import View, TemplateView, FormView
from django.urls import reverse_lazy


nav_menu = {
    'menu': ['Главная', 'Галерея', 'О нас', 'Курсы'],
}

class MenuMixin(View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = nav_menu['menu']
        return context

class NewsContent(MenuMixin, TemplateView):
    template_name = 'blog/news.html'
    extra_context = {'title': 'Новости'}


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

class Gallery(MenuMixin, TemplateView):
    template_name = 'blog/gallery.html'
    extra_context = {'title': 'Галерея'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = ImageGroup.objects.all()
        context['menu'] = nav_menu['menu']
        return context



class AddNews(LoginRequiredMixin, MenuMixin, FormView):
    template_name = 'blog/add_news.html'
    extra_context = {'title': 'Добавить новость'}
    form_class = NewsForm
    success_url = '/'
    login_url = reverse_lazy('users:login')
    redirect_field_name = 'next'
    

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)



class About(MenuMixin, TemplateView):
    template_name = 'blog/about.html'
    extra_context = {'title': 'О нас'}



class Authorization(MenuMixin, FormView):
    template_name = 'blog/authorization.html'
    extra_context = {'title': 'Авторизация'}
    form_class = AuthorizationForm
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)
