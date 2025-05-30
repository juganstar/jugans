from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views
from .views import about_view

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('post/new/', views.create_post, name='create_post'),
    path('review/', views.post_review, name='post_review'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('post/approve/<int:pk>/', views.approve_post, name='approve_post'),
    path('post/reject/<int:pk>/', views.reject_post, name='reject_post'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
         name='password_reset_complete'),
     path('search/', views.search, name='search'),
     path('about/', about_view, name='about'),
     path('accounts/', include('allauth.urls')),
]