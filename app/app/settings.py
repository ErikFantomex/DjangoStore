import os
from pathlib import Path

from decouple import Csv, config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    'DJANGO_SECRET_KEY',
    default='django-insecure-development-key-change-in-production',
)
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config(
    'DJANGO_ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=Csv(),
)
CSRF_TRUSTED_ORIGINS = config(
    'DJANGO_CSRF_TRUSTED_ORIGINS',
    default='',
    cast=Csv(),
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_htmx',
    'corsheaders',
    'core',
    'rest_framework.authtoken',
    'rest_framework',
    'drf_spectacular',
    'user',
    'recipe',
    'food',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],
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

WSGI_APPLICATION = 'app.wsgi.application'

if os.environ.get('DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': os.environ.get('DB_HOST'),
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASS'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = config('MEDIA_ROOT', default='/vol/web/media')
STATIC_ROOT = config('STATIC_ROOT', default='/vol/web/static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'core.User'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
SPECTACULAR_SETTINGS = {
    'COMPONENT_SPLIT_REQUEST': True,
}

SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

CORS_ALLOW_ALL_ORIGINS = config(
    'CORS_ALLOW_ALL_ORIGINS',
    default=False,
    cast=bool,
)
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:4200,http://127.0.0.1:4200',
    cast=Csv(),
)

SECURE_SSL_REDIRECT = config(
    'DJANGO_SECURE_SSL_REDIRECT',
    default=False,
    cast=bool,
)
SESSION_COOKIE_SECURE = config(
    'DJANGO_SESSION_COOKIE_SECURE',
    default=False,
    cast=bool,
)
CSRF_COOKIE_SECURE = config(
    'DJANGO_CSRF_COOKIE_SECURE',
    default=False,
    cast=bool,
)
