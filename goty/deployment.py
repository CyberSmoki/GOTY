import os
from .settings import *
from .settings import BASE_DIR

# which URLs can be served by this api
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] # automatically created by azure
CSRF_TRUSTED_ORIGINS = ['https://'+os.environ['WEBSITE_HOSTNAME']]
DEBUG = True # change to false  later

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = ('whitenoise.storage.CompressedManifestStaticFilesStorage')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DATABASES = {
    'default': {
            'ENGINE': 'mssql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '1433'),
            'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': (
                'Persist Security Info=False;'
                'MultipleActiveResultSets=False;'
                'Encrypt=yes;'
                'TrustServerCertificate=yes;'
                'Connection Timeout=30;'
                'Encrypt=False;'
                ),
            },
    },
}