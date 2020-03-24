import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTIngs_MODULE', 'mcur.settings')

app = Celery('mcur')

# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()