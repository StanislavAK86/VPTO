from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login_users(request):
    return HttpResponse("Вы вошли в систему")

def logout_users(request):
    return HttpResponse("Вы вышли из системы")