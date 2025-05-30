"""
Django settings for jugans project - Final Clean Version
"""

from pathlib import Path
import sys
import os
import dj_database_url
from dotenv import load_dotenv
from utils.profanity_filter import setup_profanity_filter
from urllib.parse import urlparse
import logging

setup_profanity_filter()

# ====== Initial Setup ======
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
sys.path.append(str(BASE_DIR))

# ====== Core Configuration ======
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key-only')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'jugans.onrender.com',
    '.onrender.com'
]

# Render.com specific settings
RENDER = os.getenv('RENDER', 'False').lower() == 'true'

# ====== Application Definition ======
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    
    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Providers
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    
    # Local apps
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
]

# ====== Templates Configuration ======
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ====== Authentication Settings ======
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Modern allauth configuration (non-deprecated)
SOCIALACCOUNT_ADAPTER = 'users.adapters.NoSignupSocialAccountAdapter'

ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_SIGNUP_FIELDS = ['username', 'password1', 'password2']
ACCOUNT_LOGOUT_ON_GET = True

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# OAuth providers
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
            'secret': os.getenv('GOOGLE_SECRET_KEY', ''),
        }
    },
    'github': {
        'SCOPE': ['user', 'user:email'],
        'APP': {
            'client_id': os.getenv('GITHUB_CLIENT_ID', ''),
            'secret': os.getenv('GITHUB_SECRET_KEY', ''),
        }
    }
}

# ====== Middleware ======
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# ====== Database ======
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Production (Render)
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=RENDER
        )
    }
else:
    # Local Docker development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mydb',
            'USER': 'myuser',
            'PASSWORD': 'mypass',
            'HOST': 'db',  # Matches docker-compose service name
            'PORT': '5432',
        }
    }

# ====== Static Files ======
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ====== Security ======
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ====== Email (Disabled) ======
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# ====== URL Configuration ======
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ====== Internationalization ======
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ====== Password Validation ======
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'My Portfolio Blog API',
    'DESCRIPTION': 'Professional API for my Django blog project',
    'VERSION': '1.0.0',
    'SWAGGER_UI_DIST': 'SIDECAR',  # Embeds Swagger UI
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
}

logging.basicConfig(level=logging.DEBUG)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'allauth': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}