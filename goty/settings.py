import environ
import os
from pathlib import Path

env = environ.Env(
    DEBUG=(bool, False),
    DB_EXTRA_PARAMS=(str, ""),
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

API_ENDPOINT = env('API_ENDPOINT')
CLIENT_ID = env('CLIENT_ID')
CLIENT_SECRET = env('CLIENT_SECRET')
REDIRECT_URI = env('REDIRECT_URI')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.sessions'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware'
]

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'OPTIONS': {
            'driver': env('DB_DRIVER'),
            'extra_params': env('DB_EXTRA_PARAMS'),
        }
    }
}

DATABASE_CONNECTION_POOLING = False

ROOT_URLCONF = 'goty.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'goty.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
