from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.context_processors import request
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, View





class MenuMixin(View):
    nav_menu = {
        'menu': ['Главная', 'Галерея', 'О нас', 'Курсы'],
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.nav_menu['menu']
        return context
    
class CursesView(MenuMixin, TemplateView):
    template_name = 'curses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class QuestionnaireView(MenuMixin, TemplateView):
    template_name = 'curses/question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
# Create your views here.
# def curses(request):
#     context = {'menu': nav_menu['menu']}
#     return render(request, 'curses.html', context=context)

# def questionnaire(request):
#     context = {'menu': nav_menu['menu']}
#     return render(request, 'curses/question.html', context=context)

