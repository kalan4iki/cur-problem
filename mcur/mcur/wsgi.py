"""
WSGI config for mcur project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application
#from whitenoise.django import DjangoWhiteNoise
sys.path.append('/var/www/cur-problem/mcur')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcur.settings')

application = get_wsgi_application()
#application = DjangoWhiteNoise(application)
