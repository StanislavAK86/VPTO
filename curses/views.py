from django.core.cache import cache
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.context_processors import request
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import Cards, VideoCurses, CategoryCards
from django.shortcuts import get_object_or_404
from blog.views import MenuMixin
from django.http import StreamingHttpResponse
from .forms import VideoCursesForm
from django.views.generic.edit import CreateView, DeleteView

import logging





# class MenuMixin(View):
#     nav_menu = {
#         'menu': ['Главная', 'Галерея', 'О нас', 'Курсы'],
#     }

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['menu'] = self.nav_menu['menu']
    #     return context

class CursesView(LoginRequiredMixin, MenuMixin, TemplateView):
    template_name = 'curses.html'
    login_url = reverse_lazy('users:login')
    extra_context = {'title': 'Курсы'}
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = Cards.objects.all()
        context['show_survey'] = True  # Добавляем переменную для отображения опросника
        return context 

class QuestionnaireView(MenuMixin, TemplateView):
    template_name = 'curses/question.html'
    extra_context = {'title': 'Курсы'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class VideoView(MenuMixin, TemplateView):
    template_name = 'curses/card_list.html'
    extra_context = {'title': 'Курсы'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(CategoryCards, id=category_id)
        context['category'] = category

        cache_key = f'videos_category_{category_id}'
        videos = cache.get(cache_key)
        if not videos:
            videos = VideoCurses.objects.filter(category=category)
            cache.set(cache_key, videos, 60 * 1)  # Кеширование на 15 минут

        context['videos'] = videos
        return context


class VideoStreamView(View):
    def get(self, request, video_id):
        video = get_object_or_404(VideoCurses, id=video_id)
        file = video.file
        response = StreamingHttpResponse(file.chunks(), content_type='video/mp4')
        response['Content-Disposition'] = f'inline; filename="{file.name}"'
        return response
    

class VideoCreateView(UserPassesTestMixin, MenuMixin, CreateView):
    model = VideoCurses
    form_class = VideoCursesForm
    template_name = 'curses/video_form.html'
    success_url = reverse_lazy('video_add') 

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='moderator').exists()

    def form_valid(self, form):
        form.instance.file_hash = form.instance.calculate_file_hash(form.instance.file)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'add_video'  
        return context

logger = logging.getLogger(__name__)

class VideoDeleteView(MenuMixin, LoginRequiredMixin, DeleteView):
    model = VideoCurses
    template_name = 'curses/video_confirm_delete.html'
    success_url = reverse_lazy('Курсы')

    def form_valid(self, form):
        try:
            self.object = self.get_object()
            file_path = self.object.file.path
            logger.info(f"Deleting file at path: {file_path}")
            success_url = self.get_success_url()
            self.object.delete()
            default_storage.delete(file_path)
            logger.info(f"Successfully deleted object with pk: {self.object.pk}")
            return HttpResponseRedirect(success_url)
        except Exception as e:
            logger.error(f"Error deleting object: {e}")
            return HttpResponseRedirect(success_url)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj is None:
            logger.error(f"Object with pk {self.kwargs['pk']} not found")
        return obj
    