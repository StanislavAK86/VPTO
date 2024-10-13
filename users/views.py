from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .forms import (
    CustomAuthenticationForm,
    RegistrationForm,
    ProfileUserform,
    UserPasswordChangeForm
)
from django.views.generic import TemplateView, View, FormView, CreateView
from django.views.generic.edit import UpdateView
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
    success_url = reverse_lazy('Главная')  # URL для перенаправления после успешной аутентификации
    

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.POST.get('next')
        return reverse_lazy('Главная')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            next_url = self.request.GET.get('next', reverse_lazy('Главная'))
            return redirect(next_url)
        else:
            form.add_error(None, "Invalid username or password")
            return self.form_invalid(form)
    

class LogoutUsersView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('users:login'))
    

class RegistrationView(MenuMixin, FormView):
    template_name = 'users/registration.html'
    form_class = RegistrationForm
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Регистрация прошла успешно. Теперь вы можете войти.')
        return super().form_valid(form)
    


class ProfileUser(LoginRequiredMixin, MenuMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserform
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль пользователя', 'active_tab': 'profile'}

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.pk})
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Ваш профиль успешно обновлен.')
        return super().form_valid(form)

class UserPasswordChange(MenuMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    extra_context = {'title': 'Изменение пароля', 'active_tab': 'password_change'}
    success_url = reverse_lazy('users:password_change_done')


    def form_valid(self, form):
        messages.success(self.request, 'Ваш пароль успешно изменен.')
        return super().form_valid(form)


class UserPasswordChangeDone(MenuMixin, TemplateView):
    template_name = 'users/password_change_done.html'
    extra_context = {'title': 'Смена пароля завершена'}

