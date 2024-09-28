from django.urls import path
from . import views
from .views import LoginUserView, LogoutUsersView

app_name = "users"

urlpatterns = [
    path('login/', LoginUserView.as_view(), name="login"),
    path('logout/', LogoutUsersView.as_view(), name="logout"),
]