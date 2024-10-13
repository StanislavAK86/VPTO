from django.urls import path
from . import views
from .views import (LoginUserView,
                    LogoutUsersView,
                    RegistrationView,
                    ProfileUser,
                    UserPasswordChange,
                    UserPasswordChangeDone
                    )

app_name = "users"

urlpatterns = [
    path('login/', LoginUserView.as_view(), name="login"),
    path('logout/', LogoutUsersView.as_view(), name="logout"),
    path('signup/', views.RegistrationView.as_view(), name="signup"),
    path('profile/<int:pk>/', ProfileUser.as_view(), name='profile'),
    path('password_change/', UserPasswordChange.as_view(), name="password_change"),
    path('password_change_done/', UserPasswordChangeDone.as_view(), name='password_change_done'),

]