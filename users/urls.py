from django.urls import path
from . import views
from .views import LoginUserView, LogoutUsersView, RegistrationView

app_name = "users"

urlpatterns = [
    path('login/', LoginUserView.as_view(), name="login"),
    path('logout/', LogoutUsersView.as_view(), name="logout"),
    path('signup/', views.RegistrationView.as_view(), name="signup"),
]