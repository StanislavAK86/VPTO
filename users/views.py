from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .forms import CustomAuthenticationForm
from django.views.generic import TemplateView, View, FormView
from django.urls import reverse_lazy

class MenuMixin(View):
    nav_menu = {
        'menu': ['Главная', 'Галерея', 'О нас', 'Курсы'],
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.nav_menu['menu']
        return context
# Create your views here.


class LoginUserView(MenuMixin, FormView):
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('users:Главная')  # URL для перенаправления после успешной аутентификации

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.POST.get('next')
        return reverse_lazy('users:Главная')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            next_url = self.request.GET.get('next', 'users:login')
            return redirect(next_url)
        else:
            form.add_error(None, "Invalid username or password")
            return self.form_invalid(form)
    

class LogoutUsersView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('users:login'))