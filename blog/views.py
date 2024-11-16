from .models import News
from .models import ImageGroup, Image
from .forms import NewsForm, AuthorizationForm, editImageForm, ImageGroupForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.template.context_processors import request
from django.views.decorators.cache import cache_page
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, TemplateView, FormView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
import os




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
    list_per_page = 10

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

        # Пагинация
        paginator = Paginator(news, self.list_per_page)
        page = self.request.GET.get('page')

        try:
            news_page = paginator.page(page)
        except PageNotAnInteger:
            news_page = paginator.page(1)
        except EmptyPage:
            news_page = paginator.page(paginator.num_pages)

        context['news'] = news_page
        return context

class Gallery(MenuMixin, TemplateView):
    template_name = 'blog/gallery.html'
    extra_context = {'title': 'Галерея'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = ImageGroup.objects.all()
        context['menu'] = nav_menu['menu']
        return context

class ImageGroupCreateView(MenuMixin, UserPassesTestMixin, CreateView):
    model = ImageGroup
    form_class = ImageGroupForm
    template_name = 'blog/imagegroup_form.html'
    success_url = reverse_lazy('Галерея')

    def test_func(self):
        
        return self.request.user.is_superuser or self.request.user.groups.filter(name='moderator').exists()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'imagegroup_add'  
        return context
class ImageUpdateView(UserPassesTestMixin, UpdateView):
    model = Image
    form_class = editImageForm
    template_name = 'blog/edit_image_form.html'
    success_url = reverse_lazy('Галерея')  
    def test_func(self):
        
        return self.request.user.is_superuser or self.request.user.groups.filter(name='moderator').exists()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = nav_menu['menu']
        return context
class ImageCreateView(UserPassesTestMixin, CreateView):
    model = Image
    form_class = editImageForm
    template_name = 'blog/edit_image_form.html'
    success_url = reverse_lazy('Галерея')  

    def test_func(self):
        
        return self.request.user.is_superuser or self.request.user.groups.filter(name='moderator').exists()
    def get_initial(self):
        initial = super().get_initial()
        group_id = self.request.GET.get('group')
        if group_id:
            initial['group'] = group_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = nav_menu['menu']
        return context

    def form_valid(self, form):
        images = self.request.FILES.getlist('image')
        if images:
            for image in images:
                Image.objects.create(
                    group=form.cleaned_data['group'],
                    image=image,
                    description=form.cleaned_data['description']
                )
        return redirect(self.success_url)
class ImageDeleteView(UserPassesTestMixin, DeleteView):
    model = Image
    template_name = 'blog/image_confirm_delete.html'
    success_url = reverse_lazy('Галерея')  
    def test_func(self):
        
        return self.request.user.is_superuser or self.request.user.groups.filter(name='moderator').exists()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = nav_menu['menu']
        context['image'] = self.get_object().image
        return context

    def form_valid(self, form):
        self.object = self.get_object()
        if self.object.image:  
            if os.path.isfile(self.object.image.path):
                os.remove(self.object.image.path)
        
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
class AddNews(LoginRequiredMixin, PermissionRequiredMixin, MenuMixin, FormView, UserPassesTestMixin):
    template_name = 'blog/add_news.html'
    extra_context = {'title': 'Добавить новость'}
    form_class = NewsForm
    login_url = reverse_lazy('users:login')
    redirect_field_name = 'next'
    permission_required = 'blog.add_news'
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Moderator').exists()

    def form_valid(self, form):
        news = form.save(commit=False)
        news.autor = self.request.user
        news.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.request.user.pk})
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'add_news'  # Добавляем переменную active_tab в контекст
        return context


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
