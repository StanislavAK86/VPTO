from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.context_processors import request
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Cards, VideoCurses, CategoryCards
from django.shortcuts import get_object_or_404





class MenuMixin(View):
    nav_menu = {
        'menu': ['Главная', 'Галерея', 'О нас', 'Курсы'],
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.nav_menu['menu']
        return context
    
class CursesView(LoginRequiredMixin, MenuMixin, TemplateView):
    template_name = 'curses.html'
    login_url = reverse_lazy('users:login')
    extra_context = {'title': 'Курсы'}
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = Cards.objects.all()
        return context

class QuestionnaireView(MenuMixin, TemplateView):
    template_name = 'curses/question.html'
    extra_context = {'title': 'Курсы'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
# классовое представление показа видео по катигориям

class VideoView(MenuMixin, TemplateView):
    template_name = 'curses/card_list.html'
    extra_context = {'title': 'Курсы'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(CategoryCards, id=category_id)
        context['category'] = category
        context['videos'] = VideoCurses.objects.filter(category=category)
        return context

    


