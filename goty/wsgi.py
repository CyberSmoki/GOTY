"""
WSGI config for goty project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# automatically change used settings file depending if server is hosted locally or on Azure
settings_module = 'goty.deployment' if 'DEPLOYMENT' in os.environ else 'goty.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
