from django.urls import path
from .views import register, profile, CustomLoginView
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', LogoutView.as_view(next_page='blog:home'), name='logout'),
]