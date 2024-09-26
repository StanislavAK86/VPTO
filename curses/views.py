from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.context_processors import request
from django.views.decorators.cache import cache_page


nav_menu = {
    'menu': ['Главная', 'Галерея', 'О нас', 'Курсы'],
}
# Create your views here.
def curses(request):
    context = {'menu': nav_menu['menu']}
    return render(request, 'curses/curses.html', context=context)
