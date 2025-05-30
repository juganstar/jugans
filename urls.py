from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from blog.api import PostViewSet, CategoryViewSet, CommentViewSet
from allauth.socialaccount.providers.github.views import oauth2_login as github_login
from allauth.socialaccount.providers.google.views import oauth2_login as google_login
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from django.conf import settings
from django.views.defaults import permission_denied
from django.shortcuts import render
from rest_framework.schemas import get_schema_view

# API Router Configuration
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    # Admin Site
    path('admin/', admin.site.urls),
    
    # User management
    path('users/', include('users.urls')),
    
    # Blog App
    path('', include('blog.urls')),
    
    # API Routes
    path('api/', include(router.urls)),  # This includes all API endpoints
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Authentication
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    # Social Auth
    path('accounts/', include('allauth.urls')),
    path('accounts/github/login/', github_login, name='github_login'),
    path('accounts/google/login/', google_login, name='google_login'),
    
    # Password Reset
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    # Health Check
    path('health/', TemplateView.as_view(template_name='health_check.html'), name='health_check'),
    path('api/test-schema/', get_schema_view(title="Test Schema"), name='test-schema'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

def handler403(request, exception=None):
    return render(request, '403.html', status=403)